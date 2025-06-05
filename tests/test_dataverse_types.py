import unittest

from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseCollection


class TestDataverseTypes(unittest.TestCase):
    def test_dataverse_collection(self):
        dataverse_collection = DataverseCollection()
        dataverse_collection.dataverse_type = "TYPE"
        dataverse_collection.collection_name = "COLLECTION"
        dataverse_collection.collection_alias = "COLLECTION_ALIAS"
        dataverse_collection.collection_name = "COLLECTION_NAME"
        dataverse_collection.collection_parent = "Accelerator Dataverse"
        dataverse_collection.dataverse_contacts.append("<EMAIL>")
        dataverse_collection.dataverse_contacts.append("<EMAIL2>")
        dataverse_collection.affiliation = "AFFILIATION"

        json = dataverse_collection.render()

        self.assertIsNotNone(json)




if __name__ == '__main__':
    unittest.main()
