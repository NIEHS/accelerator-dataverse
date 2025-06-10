import unittest

from accelerator_dataverse.dataverse_utils.dataverse_config import DataverseConfig
from accelerator_dataverse.dataverse_utils.dataverse_connector import DataverseConnector
from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseCollection


class TestDataverseConnector(unittest.TestCase):

    def test_add_dataverse(self):
        dataverse_config = DataverseConfig.from_env()
        dataverse_connector = DataverseConnector(dataverse_config=dataverse_config)
        dataverse_collection = DataverseCollection()
        dataverse_collection.collection_name = "test_dataverse_connector"
        dataverse_collection.dataverse_contacts.append("test@test.com")
        dataverse_collection.collection_alias = "test_dataverse_collection_alias"
        dataverse_collection.affiliation = "NIEHS"
        dataverse_collection.description = "Test Dataverse"
        dataverse_collection.collection_parent = "Root"

        dataverse_connector.delete_dataverse(dataverse_collection.collection_alias)
        dataverse_connector.add_dataverse(dataverse_collection=dataverse_collection)

    def test_get_version(self):
        dataverse_config = DataverseConfig.from_env()
        dataverse_connector = DataverseConnector(dataverse_config=dataverse_config)
        version = dataverse_connector.get_version()
        self.assertIsNotNone(version)


if __name__ == '__main__':
    unittest.main()
