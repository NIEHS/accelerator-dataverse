from accelerator_core.utils.logger import setup_logger
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataverse

from accelerator_dataverse.dataverse_utils.dataverse_config import DataverseConfig
from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseCollection, DataverseDataset

logger = setup_logger("accelerator-dataverse")

class AbstractDataverseConnector:
    """
    Abstract superclass for a DataverseConnector. This allows easy mocking and/or integration into
    environments such as Airflow.
    """

    def __init__(self, dataverse_config:DataverseConfig):
        self.dataverse_config = dataverse_config

    def add_dataverse(self, dataverse_collection:DataverseCollection):
       pass


class DataverseConnector(AbstractDataverseConnector):
    """
    Connector to dataverse using Dataverse API
    """
    def __init__(self, dataverse_config:DataverseConfig):
        super().__init__(dataverse_config)
        self.api = NativeApi(dataverse_config.dataverse_host, dataverse_config.api_key)

    def get_version(self):
        resp = self.api.get_info_version()
        return resp

    def add_dataverse(self, dataverse_collection:DataverseCollection):
        logger.info("adding collection: {}".format(dataverse_collection))
        payload = dataverse_collection.render()
        dv = Dataverse()
        dv.from_json(payload)

        resp = self.api.create_dataverse(dataverse_collection.collection_parent, dv.json())
        logger.info("response: {}".format(resp))
        if resp.is_error:
            logger.error("ERROR - Could not create dataverse collection: {}".format(resp))
            raise Exception("ERROR - Could not create dataverse collection: {}".format(resp))

    def delete_dataverse(self, dataverse_id:str):
        """
        Idempotent delete of dataverse by alias or id.
        :param dataverse_id: str with dataverse alias or id
        :return: None
        """

        logger.info(f"delete dataverse with alias: {{dataverse_id}}")
        try:
            self.api.delete_dataverse(dataverse_id)
        except Exception as e:
            logger.info("ignoring delete exception: {}".format(e))

    def verify_target_dataverse(self, dataverse_id:str) -> bool:
        """
        Verify that the target dataverse exists.
        :param dataverse_id: id or alias for target dataverse
        :return: bool of True if target dataverse exists
        """
        logger.info(f"verify target dataverse with alias: {{dataverse_id}}")

        resp = self.api.get_dataverse(dataverse_id)
        logger.info("response: {}".format(resp))
        return resp.is_success

    def create_dataset(self, dataverse:str, dataverse_dataset:DataverseDataset):
        """
        Create a dataverse dataset.
        :param dataverse: dataverse to create collection within
        :param dataverse_dataset:
        :return: TODO: determine return type
        """

        logger.info(f"create dataset: {dataverse_dataset}")
        payload = dataverse_dataset.render()
        resp = self.api.create_dataset(dataverse, payload, publish=False)
        logger.info("response: {}".format(resp))
        return resp.is_success

    def delete_dataset(self, dataset_id:str) -> bool:
        logger.info(f"delete dataset: {dataset_id}")
        resp = self.api.delete_dataset(dataset_id)
        logger.info("response: {}".format(resp))
