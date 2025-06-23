import json

from accelerator_core.utils.logger import setup_logger
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataverse

from accelerator_dataverse.dataverse_utils.dataverse_config import DataverseConfig
from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseCollection, DataverseDataset

logger = setup_logger("accelerator-dataverse")


class DataverseListing:
    """
    Data structure holding result of a 'list datasets in a dataverse collection'
    """

    def __init__(self):
        self.id = 0
        self.identifier = ""
        self.persistent_url = ""
        self.protocol = ""
        self.authority = ""
        self.separator = "/"
        self.publisher = ""
        self.storage_identifier = ""
        self.dataset_type = ""
        self.type = ""


    @staticmethod
    def from_json(json_data:dict):
        """
        From a dict representation from the API, return a DataverseListing object.
        :param json_data: dict with entry
        :return: DataverseListing for that entry
        """

        listing = DataverseListing()
        listing.id = json_data["id"]
        listing.identifier = json_data["identifier"]
        listing.persistent_url = json_data["persistentUrl"]
        listing.protocol = json_data["protocol"]
        listing.authority = json_data["authority"]
        listing.separator = json_data["separator"]
        listing.publisher = json_data["publisher"]
        listing.storage_identifier = json_data["storageIdentifier"]
        listing.dataset_type = json_data["datasetType"]
        listing.type = json_data["type"]
        return listing


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

    def delete_dataverse(self, dataverse_id:str, clear_datasets:bool=False):
        """
        Idempotent delete of dataverse by alias or id.
        :param dataverse_id: str with dataverse alias or id
        :param clear_datasets: clear datasets before deletion
        :return: None
        """

        logger.info(f"delete dataverse with alias: {{dataverse_id}}")

        if clear_datasets:
            logger.info(f"clear datasets before deletion: {{dataverse_id}}")
            datasets = self.list_dataverse_contents(dataverse_id)
            if datasets:
                logger.info("have datasets to delete")
                for dataset in datasets:
                    logger.info(f"delete dataset: {dataset}")
                    self.delete_dataverse_collection(dataset.identifier)

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

    def list_dataverse_contents(self, dataverse_id:str) -> [DataverseListing]:
        """
        Given the id of a dataverse, list the contents of the dataverse.
        :param dataverse_id: str with dataverse alias or id
        :return: [DataverseListing]
        """

        logger.info(f"listing dataverse contents for {dataverse_id}")
        resp = self.api.get_dataverse_contents(dataverse_id)
        logger.debug("response: {}".format(resp))

        if resp.is_error:
            logger.error("ERROR - Could not list dataverse contents: {}".format(resp))
            raise Exception("ERROR - Could not list dataverse contents: {}".format(resp))

        respdata = json.loads(resp.content)
        listing = []
        for entry in respdata["data"]:
            listing.append(DataverseListing.from_json(entry))

        return listing

    def delete_dataverse_collection(self, collection_pid):
        """
        Delete a collection.
        :param collection_pid: collection pid to delete
        :return: bool of True if collection was deleted
        """

        logger.info(f"deleting collection {collection_pid}")
        self.api.delete_dataset(collection_pid, is_pid=True)

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
        if not resp.is_success:
            logger.warning("ERROR - Could not create dataverse dataset: {}".format(resp.content))
        return resp.is_success

    def delete_dataset(self, dataset_id:str) -> bool:
        logger.info(f"delete dataset: {dataset_id}")
        resp = self.api.delete_dataset(dataset_id)
        logger.info("response: {}".format(resp))



