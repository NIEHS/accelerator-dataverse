import unittest

from accelerator_dataverse.dataverse_utils.dataverse_config import DataverseConfig
from accelerator_dataverse.dataverse_utils.dataverse_connector import DataverseConnector
from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseCollection, DataverseDataset, \
    CitationMetadataBlock, CitationAuthor, DatasetContact, DatasetDescription, DatasetKeyword, TopicClassification, \
    Publication, OtherId


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

    def test_verify_dataverse(self):
        dataverse_config = DataverseConfig.from_env()
        dataverse_connector = DataverseConnector(dataverse_config=dataverse_config)
        dataverse_present = dataverse_connector.verify_target_dataverse("Root")
        self.assertTrue(dataverse_present)

    def test_get_version(self):
        dataverse_config = DataverseConfig.from_env()
        dataverse_connector = DataverseConnector(dataverse_config=dataverse_config)
        version = dataverse_connector.get_version()
        self.assertIsNotNone(version)

    def test_create_dataset(self):
        dataverse_config = DataverseConfig.from_env()
        dataverse_connector = DataverseConnector(dataverse_config=dataverse_config)
        dataverse_collection = DataverseCollection()
        dataverse_collection.collection_name = "test_create_dataset"
        dataverse_collection.dataverse_contacts.append("testid@nih.gov")
        dataverse_collection.collection_alias = "test_create_dataset_alias"
        dataverse_collection.affiliation = "NIEHS"
        dataverse_collection.description = "Test Dataverse"
        dataverse_collection.collection_parent = "Root"

        #dataverse_connector.delete_dataverse(dataverse_collection.collection_alias)
        #dataverse_connector.add_dataverse(dataverse_collection=dataverse_collection)


        # create a new dataset underneath this collection

        dataset = DataverseDataset()
        dataset.protocol = "protocol"
        dataset.authority = "authority"
        dataset.identifier = "test_create_dataset"

        dataset.license.name = "CC0 1.0"
        dataset.license.url = "http://creativecommons.org/licenses/by/2.0/"

        citation_block = CitationMetadataBlock()
        citation_block.title = "title"
        citation_block.subtitle = "subtitle"
        citation_block.alternative_title.append("alternative_title")
        citation_block.alternative_url = "alternative_url"

        other_id = OtherId()
        other_id.agency = "agency"
        other_id.value = "value"

        citation_block.other_id.append(other_id)

        citation_block.other_id = "other_id"
        citation_block.other_id_agency = "other_id_agency"
        citation_block.other_id_value = "other_id_value"

        author = CitationAuthor()
        author.author_name = "author_name"
        author.author_affiliation = "author_affiliation"
        author.author_identifier_scheme = "author_identifier_scheme"
        author.author_identifier = "author_identifier"

        citation_block.author.append(author)

        contact = DatasetContact()
        contact.contact_name = "contact_name"
        contact.contact_affiliation = "contact_affiliation"
        contact.contact_email = "contact_email@mail.com"

        citation_block.dataset_contact.append(contact)

        dataset_description = DatasetDescription()
        dataset_description.description = "dataset_description"
        dataset_description.description_text = "dataset_description_date"


        citation_block.dataset_description.append(dataset_description)

        citation_block.subject = ["Chemistry"]

        keyword = DatasetKeyword()
        keyword.keyword = "keyword"
        keyword.keyword_uri = "keyword_uri"
        keyword.vocabulary = "vocabulary"
        keyword.vocabulary_uri = "vocabulary_uri"

        citation_block.keyword.append(keyword)

        topic = TopicClassification()
        topic.topic_name = "topic_name"
        topic.vocabulary_uri = "vocabulary_uri"
        topic.vocabulary = "vocabulary"

        citation_block.topic_classification.append(topic)

        publication = Publication()
        publication.publication_name = "publication_relation_type"
        publication.citation = "publication_citation"
        publication.id_type = "publication_id_type"
        publication.id_number = "publication_id_number"
        publication.url = "publication_url"

        citation_block.publication.append(publication)

        citation_block.notes_text = "notes_text"

        dataset.citation = citation_block

        actual = dataverse_connector.create_dataset(dataverse_collection.collection_alias, dataverse_dataset=dataset)

        self.assertTrue(actual)

    def test_delete_dataset(self):
        dataverse_config = DataverseConfig.from_env()
        dataverse_connector = DataverseConnector(dataverse_config=dataverse_config)
        dataverse_collection = DataverseCollection()
        dataverse_collection.collection_name = "test_delete_dataset"
        dataverse_collection.dataverse_contacts.append("testid@nih.gov")
        dataverse_collection.collection_alias = "test_delete_dataset_alias"
        dataverse_collection.affiliation = "NIEHS"
        dataverse_collection.description = "Test Dataverse"
        dataverse_collection.collection_parent = "Root"

        # dataverse_connector.delete_dataverse(dataverse_collection.collection_alias)
        #   dataverse_connector.add_dataverse(dataverse_collection=dataverse_collection)

        # create a new dataset underneath this collection

        dataset = DataverseDataset()
        dataset.protocol = "protocol"
        dataset.authority = "authority"
        dataset.identifier = "test_delete_dataset"

        dataset.license.name = "CC0 1.0"
        dataset.license.url = "http://creativecommons.org/licenses/by/2.0/"

        citation_block = CitationMetadataBlock()
        citation_block.title = "title"
        citation_block.subtitle = "subtitle"
        citation_block.alternative_url = "alternative_url"
        citation_block.other_id = "other_id"
        citation_block.other_id_agency = "other_id_agency"
        citation_block.other_id_value = "other_id_value"

        author = CitationAuthor()
        author.author_name = "author_name"
        author.author_affiliation = "author_affiliation"
        author.author_identifier_scheme = "author_identifier_scheme"
        author.author_identifier = "author_identifier"

        citation_block.author.append(author)

        contact = DatasetContact()
        contact.contact_name = "contact_name"
        contact.contact_affiliation = "contact_affiliation"
        contact.contact_email = "contact_email@mail.com"

        citation_block.dataset_contact.append(contact)

        dataset_description = DatasetDescription()
        dataset_description.description = "dataset_description"
        dataset_description.description_text = "dataset_description_date"

        citation_block.dataset_description.append(dataset_description)

        citation_block.subject = ["Chemistry"]

        keyword = DatasetKeyword()
        keyword.keyword = "keyword"
        keyword.keyword_uri = "keyword_uri"
        keyword.vocabulary = "vocabulary"
        keyword.vocabulary_uri = "vocabulary_uri"

        citation_block.keyword.append(keyword)

        topic = TopicClassification()
        topic.topic_name = "topic_name"
        topic.vocabulary_uri = "vocabulary_uri"
        topic.vocabulary = "vocabulary"

        citation_block.topic_classification.append(topic)

        publication = Publication()
        publication.publication_name = "publication_relation_type"
        publication.citation = "publication_citation"
        publication.id_type = "publication_id_type"
        publication.id_number = "publication_id_number"
        publication.url = "publication_url"

        citation_block.publication.append(publication)

        citation_block.notes_text = "notes_text"

        dataset.citation = citation_block

        #created = dataverse_connector.create_dataset(dataverse_collection.collection_alias, dataverse_dataset=dataset)

        #self.assertTrue(created)
        # now delete
        dataset.identifier = "https://doi.org/10.5072/FK2/HO2RH6"
        deleted = dataverse_connector.delete_dataset(dataset.identifier)
        self.assertTrue(deleted)




if __name__ == '__main__':
    unittest.main()
