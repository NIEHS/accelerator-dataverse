from accelerator_core.utils.logger import setup_logger

from accelerator_dataverse.dataverse_utils.dataverse_config import DataverseConfig
from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseCollection

logger = setup_logger("accelerator-dataverse")

class AbstractDataverseConnector:
    """
    Abstract superclass for a DataverseConnector. This allows easy mocking and/or integration into
    environments such as Airflow.
    """

    def __init__(self, dataverse_config:DataverseConfig):
        self.dataverse_config = dataverse_config

    def add_collection(self, dataverse_collection:DataverseCollection):
        logger.info("adding collection: {}".format(dataverse_collection))
        payload = dataverse_collection.render()


