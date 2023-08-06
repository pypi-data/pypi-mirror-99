from azureml.studio.common.io.pickle_utils import write_with_pickle
from azureml.studio.common.io.data_table_io import write_data_table
from azureml.studio.modules.datatransform.common.base_transform import BaseTransform
from azureml.studio.modules.ml.common.base_clustser import BaseCluster
from azureml.studio.modules.ml.common.base_learner import BaseLearner
from azureml.studio.modules.recommendation.common.base_recommender import BaseRecommender
from azureml.studio.common.datatable.data_table import DataTable


class Writer:
    @classmethod
    def write_into_dataset(cls, dt, file_name):
        if not isinstance(dt, DataTable):
            raise TypeError("dt must be type DataTable.")
        return write_data_table(dt, file_name)

    @classmethod
    def write_into_base_learner(cls, learner, file_name):
        if not isinstance(learner, BaseLearner):
            raise TypeError("learner must be type BaseLearner.")
        return write_with_pickle(learner, file_name)

    @classmethod
    def write_into_base_cluster(cls, cluster, file_name):
        if not isinstance(cluster, BaseCluster):
            raise TypeError("cluster must be type BaseCluster.")
        return write_with_pickle(cluster, file_name)

    @classmethod
    def write_into_base_transform(cls, transform, file_name):
        if not isinstance(transform, BaseTransform):
            raise TypeError("transform must be type BaseTransform.")
        return write_with_pickle(transform, file_name)

    @classmethod
    def write_into_base_recommender(cls, recommender, file_name):
        if not isinstance(recommender, BaseRecommender):
            raise TypeError('recommender must by type BaseRecommender.')
        return write_with_pickle(recommender, file_name)
