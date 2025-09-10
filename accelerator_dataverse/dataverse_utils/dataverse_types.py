import json

from accelerator_core.utils.data_utils import Serializable

from accelerator_dataverse.dataverse_utils.template_processor import TemplateProcessor

class DataverseCollection(Serializable):
    def __init__(self):
        self.collection_name = ""
        self.collection_alias = ""
        self.dataverse_contacts = []
        self.affiliation = ""
        self.description = ""
        self.dataverse_type = ""
        self.collection_parent = ""

    def render(self):
        template_processor = TemplateProcessor()
        template = template_processor.retrieve_template("dataverse-collection")
        return template.render(collection=self)


class DataverseDataset(Serializable):
    def __init__(self):
        self.protocol = ""
        self.authority = ""
        self.identifier = ""
        self.citation = CitationMetadataBlock()
        self.geospatial = GeospatialMetadataBlock()
        self.computational_workflow = ComputationalWorkflow()
        self.cafe_custom = CafeCustomMetadata()
        self.license = License()
        self.files = []

    def render(self):
        template_processor = TemplateProcessor()
        template = template_processor.retrieve_template("dataset-extended")
        return template.render(dataset=self)


class DataverseDatasetLicense(Serializable):
    def __init__(self, name, uri):
        self.name = name
        self.uri = uri

class CafeCustomMetadata(Serializable):

    def __init__(self):
        self.derived_from_existing_dataset = False
        self.source_data_title = ""
        self.source_data_author = []
        self.source_data_institution = ""
        self.source_version_number = ""
        self.source_data_doi_or_url = ""
        self.source_data_last_modified_date = ""
        self.source_data_date_obtained = ""
        self.source_data_type = "" # cv
        self.source_data_type_other = ""
        self.source_data_timestep = ""
        # spatial resolution not in jinja rn
        self.source_data_attribution = ""
        self.source_data_disclaimer = ""

class GeospatialMetadataBlock(Serializable):

    def __init__(self):
        self.geographic_unit = []
        self.geographic_bounding_box = [] # GeographicBoundingBox() if present


class GeographicBoundingBox(Serializable):

    def __init__(self):
        self.west = ""
        self.east = ""
        self.north = ""
        self.south = ""

class CitationMetadataBlock(Serializable):
    def __init__(self):
        self.display_name = "Citation Metadata"
        self.title = ""
        self.subtitle = ""
        self.alternative_title = []
        self.alternative_url = ""
        self.depositor = ""
        self.other_id = []
        self.author = []
        self.dataset_contact = []
        self.dataset_description = []
        self.subject = []
        self.keyword = []
        self.topic_classification = []
        self.publication = []
        self.notes_text = ""
        self.language = []
        self.producer = []
        self.production_date = ""
        self.production_place = []
        self.contributor = []
        self.grant = []
        self.distributor = []
        self.distribution_date = ""
        self.date_of_deposit = ""
        self.time_period = []
        self.date_of_collection = []
        self.kind_of_data = []
        self.series = []
        self.software = []
        self.related_material = []
        self.related_datasets = []
        self.other_references = []
        self.data_sources = []
        self.origin_of_sources = ""
        self.characteristics_of_sources_noted = ""


class CitationAuthor(Serializable):
    def __init__(self):
        self.author_name = ""
        self.author_affiliation = ""
        self.author_identifier_scheme = ""
        self.author_identifier = ""


class DatasetContact(Serializable):
    def __init__(self):
        self.contact_name = ""
        self.contact_affiliation = ""
        self.contact_email = ""


class OtherId(Serializable):
    def __init__(self):
        self.agency = ""
        self.value = ""


class DatasetDescription(Serializable):
    def __init__(self):
        self.description = ""
        self.description_date = ""


class DatasetKeyword(Serializable):
    def __init__(self):
        self.keyword = ""
        self.keyword_uri = ""
        self.vocabulary = ""
        self.vocabulary_uri = ""


class TopicClassification(Serializable):
    def __init__(self):
        self.topic_name = ""
        self.vocabulary = ""
        self.vocabulary_uri = ""


class Publication(Serializable):
    def __init__(self):
        self.publication_relation_type = ""
        self.citation = ""
        self.id_type = ""
        self.id_number = ""
        self.url = ""


class Producer(Serializable):
    def __init__(self):
        self.name = ""
        self.affiliation = ""
        self.abbreviation = ""
        self.url = ""
        self.logo_url = ""


class Contributor(Serializable):
    def __init__(self):
        self.type = ""
        self.name = ""


class Grant(Serializable):
    def __init__(self):
        self.agency = ""
        self.number = ""


class Distributor(Serializable):
    def __init__(self):
        self.name = ""
        self.affiliation = ""
        self.abbreviation = ""
        self.url = ""
        self.logo_url = ""


class TimePeriod(Serializable):
    def __init__(self):
        self.start = ""
        self.end = ""


class Series(Serializable):
    def __init__(self):
        self.name = ""
        self.information = ""


class Software(Serializable):
    def __init__(self):
        self.name = ""
        self.version = ""


class License(Serializable):
    def __init__(self):
        self.name = ""
        self.uri = ""

class ComputationalWorkflow(Serializable):
    def __init__(self):
        self.tool_type = []

class DatasetFile(Serializable):
    def __init__(self):
        self.description = ""
        self.label = ""
        self.restricted = False
        self.version = ""
        self.dataset_version_id = ""
        self.file_id = ""
        self.file_name = ""
        self.content_type = ""
        self.filesize = 0
        self.description = ""
        self.storage_identifier = ""
        self.original_format_label = ""
        self.root_data_file_id = ""
        self.checksum_type = ""
        self.checksum_value = ""
