import numpy as np
import pandas as pd
from scipy.special import softmax
from copy import deepcopy
from types import MethodType, FunctionType
from azureml.interpret import ExplanationClient
from azureml.core.run import Run, _OfflineRun
from interpret_community.mimic.models.lightgbm_model import LGBMExplainableModel
from interpret_community.mimic.models.linear_model import LinearExplainableModel
from interpret_community.common.constants import ModelTask
from interpret_community.mimic.mimic_explainer import MimicExplainer
from pandas.core.dtypes.common import is_categorical_dtype
from sklearn.model_selection import train_test_split
from azureml.studio.common.datatable.data_type_conversion import convert_column_by_element_type
from azureml.studio.common.utils.datetimeutils import convert_to_ns
from azureml.studio.modulehost.constants import ElementTypeName
from azureml.studio.modules.datatransform.common.named_encoder import _NAN_STR
from azureml.studio.modules.ml.common.mathematic_op import inf2nan, sigmoid
from azureml.studio.core.logger import TimeProfile, module_logger
from nimbusml.linear_model import PoissonRegressionRegressor
from azureml.studio.common.error import ErrorMapping
from azureml.studio.modules.ml.initialize_models.regressor.fast_forest_quantile_regressor. \
    fast_forest_quantile_regressor import FastForestQuantileRegressor
from azureml.studio.modules.ml.common.supervised_learners import RegressionLearner, \
    MultiClassificationLearner, BinaryClassificationLearner
import azureml.studio.modules.ml.initialize_models.regressor as regression_models
import azureml.studio.modules.ml.initialize_models.binary_classifier as binary_classification_models
import azureml.studio.modules.ml.initialize_models.multi_classifier as multi_classification_models
from interpret_community.dataset.dataset_wrapper import DatasetWrapper
from azureml.studio.internal.module_telemetry import ModuleTelemetryHandler
from azureml.studio.common.error import LibraryErrorInfo

EXPLANATION_SUPPORTED_LEARNERS = (
    # supported regression models
    regression_models.NeuralNetworkRegressor,
    regression_models.SGDLinearRegressor,
    regression_models.OrdinaryLeastSquaresRegressor,
    # supported binary classification models
    binary_classification_models.LogisticRegressionBiClassifier,
    binary_classification_models.SupportVectorMachineBiClassifier,
    # supported multi classification models
    multi_classification_models.DecisionForestMultiClassifier,
)


class MimicExplainerWrapper:
    MAXIMUM_EVALUATION_SAMPLES = 5000
    SPARSE_NUM_FEATURES_THRESHOLD = 1000
    EXPLAINABLE_MODEL_ARGS_STR = 'explainable_model_args'
    LINEAR_SURROGATE_SPARSE_PARAM = 'sparse_data'
    MAX_EXPLAINED_FEATURES_TO_UPLOAD = 100

    def __init__(self, model, random_state=42):
        self.random_state = random_state
        self.label_column_name = model.label_column_name
        self.numeric_features = list(model.normalizer.numeric_feature_column_encoders.keys())
        self.cat_features = list(model.normalizer.str_feature_column_encoders.keys())
        self.model = model
        self.surrogate_model, self.surrogate_model_params = self._pick_surrogate_model_with_params(model=self.model)

        if isinstance(model, (BinaryClassificationLearner, MultiClassificationLearner)):
            self.model_task = ModelTask.Classification
        elif isinstance(model, RegressionLearner) and not isinstance(model, FastForestQuantileRegressor):
            self.model_task = ModelTask.Regression
        else:
            self.model_task = None
            return

    def explain_global(self, initialization_examples: pd.DataFrame, evaluation_examples: pd.DataFrame):
        if not self.model_task:
            return

        initialization_data = self._setup_data(data=initialization_examples)
        transformations = self._setup_transformations(self.model)
        internal_model = self._setup_model(self.model)

        # We put this explainer object in the explain_global method, instead as one attribute of MimicExpalinerWrapper,
        # since this object can be very large, and we suppose it should be released after we using it in the
        # explain_global method, then the memory usage can be reduced.
        with TimeProfile("Init mimic explainer"):
            explainer = MimicExplainer(model=internal_model,
                                       initialization_examples=initialization_data,
                                       explainable_model=self.surrogate_model,
                                       explainable_model_args=self.surrogate_model_params,
                                       augment_data=False,
                                       features=[*self.numeric_features, *self.cat_features],
                                       classes=self.model.label_classes,
                                       transformations=transformations,
                                       model_task=self.model_task)

        if self.model_task == ModelTask.Classification:
            stratify_column_name = self.label_column_name
        else:
            stratify_column_name = None

        sampled_data = self._sample_data(data=evaluation_examples, sample_count=self.MAXIMUM_EVALUATION_SAMPLES,
                                         stratify_column_name=stratify_column_name)

        sampled_index = sampled_data.index
        sampled_data = self._setup_data(data=sampled_data)

        with TimeProfile("Explain global"):
            explanation = explainer.explain_global(sampled_data)

        sampled_true_labels = evaluation_examples[self.model.label_column_name].iloc[sampled_index]
        if self.model.label_column_name in self.model.normalizer.label_column_encoders:
            sampled_true_labels = self.model.normalizer.label_column_encoders[self.model.label_column_name].transform(
                sampled_true_labels)
        else:
            sampled_true_labels = sampled_true_labels.values

        return explanation, sampled_true_labels

    @classmethod
    def upload_explanation(cls, explanation, true_labels, top_k=None):
        run = Run.get_context()
        if isinstance(run, _OfflineRun) or not explanation:
            return

        client = ExplanationClient.from_run(run)

        if top_k is None:
            top_k = cls.MAX_EXPLAINED_FEATURES_TO_UPLOAD

        with TimeProfile("Upload model explanation"):
            client.upload_model_explanation(explanation, top_k=top_k, true_ys=true_labels)

    @staticmethod
    def _setup_model(model):
        def predict_proba(obj, X):
            prob = obj.decision_function(X)
            if len(prob.shape) == 2:
                prob = softmax(prob, axis=1)
            else:
                prob = sigmoid(prob)
            return prob

        interpret_model = deepcopy(model.model)
        if not hasattr(interpret_model, 'predict_proba'):
            if hasattr(interpret_model, 'decision_function'):
                interpret_model.predict_proba = MethodType(predict_proba, interpret_model)

        # workaround for poisson model, its predict method returns Series type values, and
        # this is not supported by ExplanationClient.upload_model_explanation
        if isinstance(interpret_model, PoissonRegressionRegressor):
            def predict(obj, X):
                return raw_predict(obj, X).values.ravel()

            def copy_func(func):
                return FunctionType(func.__code__, func.__globals__, func.__name__, func.__defaults__, func.__closure__)

            raw_predict = copy_func(interpret_model.predict)
            interpret_model.predict = MethodType(predict, interpret_model)

        return interpret_model

    def _setup_data(self, data: pd.DataFrame):
        # In the model.normalizer and feature encoders, we preprocess data before feeding it into the sklearn encoders.
        # This method is to do the same preprocessing to ensure model see the same data in the model explainer. The
        # preprocessing logic should be the same as we do in the training stage.
        with TimeProfile("Setup data"):
            data = data.reset_index(drop=True)

            features = {}

            # This preprocessing logic should be the same as the behavior in the Normalizer.build,
            # Normalizer._transform_numeric_feature_columns and NamedMinMaxEncoder.transform
            for numeric_col in self.numeric_features:
                feature = convert_to_ns(data[numeric_col])
                feature = inf2nan(feature)
                if np.nanstd(feature) < 1e-9:
                    feature = np.full_like(feature.values, np.nan, dtype=float)
                feature = np.nan_to_num(feature)
                features[numeric_col] = feature

            # This preprocessing logic should be the same as the behavior in the
            # Normalizer._transform_str_feature_column and NamedOneHotEncoder.transform
            for cat_col in self.cat_features:
                feature = data[cat_col]
                if is_categorical_dtype(feature.dtype):
                    if _NAN_STR not in feature.cat.categories:
                        feature = feature.cat.add_categories(_NAN_STR)
                feature.fillna(_NAN_STR, inplace=True)
                feature = convert_column_by_element_type(feature, ElementTypeName.STRING)
                features[cat_col] = feature

            data = pd.DataFrame(features, columns=[*self.numeric_features, *self.cat_features])
            data_wrapper = DatasetWrapper(data, clear_references=True)

        return data_wrapper

    @classmethod
    def _pick_surrogate_model_with_params(cls, model):
        def _transformed_feature_count(model):
            feature_count = len([enc for enc in model.normalizer.numeric_feature_column_encoders.values() if enc])
            feature_count += sum(
                [len(enc.categories[0]) for enc in model.normalizer.str_feature_column_encoders.values()])

            return feature_count

        if len(model.normalizer.str_feature_column_encoders) > 0 and _transformed_feature_count(
                model) > cls.SPARSE_NUM_FEATURES_THRESHOLD:
            surrogate_model = LinearExplainableModel
            surrogate_model_params = {cls.LINEAR_SURROGATE_SPARSE_PARAM: True}
            module_logger.info("Pick Linear Explainable Model as surrogate model.")
        else:
            surrogate_model = LGBMExplainableModel
            surrogate_model_params = {'force_col_wise': True}
            module_logger.info("Pick LGBM Explainable Model as surrogate model.")

        return surrogate_model, surrogate_model_params

    def _sample_data(self, data: pd.DataFrame, sample_count: int, stratify_column_name: str = None):
        with TimeProfile("Sample data"):
            if sample_count >= data.shape[0]:
                sampled_data = data
            else:
                stratify_column = data[stratify_column_name] if stratify_column_name is not None else None
                sample_fraction = 1.0 * sample_count / data.shape[0]
                try:
                    sampled_data, _ = train_test_split(data, train_size=sample_fraction, random_state=self.random_state,
                                                       stratify=stratify_column)
                except ValueError:
                    # if stratification fails, fall back to non-stratify train/test split
                    sampled_data, _ = train_test_split(data, train_size=sample_fraction, random_state=self.random_state)
                module_logger.info(f"Sampled dataset size: {len(sampled_data)}")

            with pd.option_context('use_inf_as_na', True):
                if self.model.label_column_name in sampled_data:
                    sampled_data = sampled_data.dropna(subset=[self.model.label_column_name])

        return sampled_data

    @staticmethod
    def _setup_transformations(model):
        cat_encoders = model.normalizer.str_feature_column_encoders
        numeric_encoders = model.normalizer.numeric_feature_column_encoders

        cat_transformations = [([feature], encoder.one_hot_encoder) for feature, encoder in cat_encoders.items() if
                               encoder]
        numeric_transformations = []

        for feature, encoder in numeric_encoders.items():
            if encoder and not encoder.unfitted:
                if encoder.std < 1e-9:
                    numeric_transformations.append(([feature], None))
                else:
                    numeric_transformations.append(([feature], encoder.encoder))
            else:
                numeric_transformations.append(([feature], None))

        # place numeric features before str features
        return numeric_transformations + cat_transformations

    @property
    def surrogate_model_name(self):
        if self.surrogate_model == LinearExplainableModel:
            return "LinearExplainableModel"
        elif self.surrogate_model == LGBMExplainableModel:
            return "LGBMExplainableModel"
        return None

    @property
    def model_type_name(self):
        if isinstance(self.model, BinaryClassificationLearner):
            return "BinaryClassification"
        elif isinstance(self.model, MultiClassificationLearner):
            return "MultiClassification"
        elif isinstance(self.model, RegressionLearner):
            return "Regression"
        return None


def explain_model(model, initialization_examples, evaluation_examples):
    if not isinstance(model, EXPLANATION_SUPPORTED_LEARNERS):
        module_logger.debug(f"For now, model {model} dose not support explanation.")
        return

    explanation = None
    surrogate_model_name = None
    model_type_name = None
    telemetry_handler = None
    session_id = None

    try:
        telemetry_handler = ModuleTelemetryHandler()
        module_logger.info("Initialize ModuleTelemetryHandler for explanation error track.")
    except Exception as ex:
        module_logger.info(f"Failed to initialize ModuleTelemetryHandler instance due to {ex}")

    try:
        from azureml._base_sdk_common import _ClientSessionId
        session_id = _ClientSessionId
    except Exception as ex:
        module_logger.info(f"Session_id cannot be imported due to {ex}")

    try:
        explainer = MimicExplainerWrapper(model=model)
        surrogate_model_name = explainer.surrogate_model_name
        model_type_name = explainer.model_type_name
        explanation, sampled_true_labels = explainer.explain_global(initialization_examples, evaluation_examples)
        explainer.upload_explanation(explanation, sampled_true_labels)
    except BaseException as e:
        module_logger.warning(f'Failed to generate model explanation. Reason:{ErrorMapping.get_exception_message(e)}. '
                              f'Please deselect "Model Explanations" option if don\'t need it.')
        error_info = LibraryErrorInfo(e)
        if telemetry_handler:
            telemetry_handler.log_telemetry(designer_event_name="ExplanationTraceback",
                                            session_id=session_id,
                                            surrogate_model=surrogate_model_name,
                                            model_type=model_type_name,
                                            traceback=error_info.traceback,
                                            error_message=error_info.message)
    else:
        if telemetry_handler:
            telemetry_handler.log_telemetry(designer_event_name="ExplanationTelemetry",
                                            session_id=session_id,
                                            surrogate_model=surrogate_model_name,
                                            model_type=model_type_name)

    return explanation
