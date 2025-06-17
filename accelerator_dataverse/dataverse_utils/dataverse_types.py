from accelerator_dataverse.dataverse_utils.template_processor import TemplateProcessor


class DataverseCollection:
    """
    Represents data model for a Dataverse collection
    see: https://guides.dataverse.org/en/latest/api/native-api.html#dataverse-collections
    """
    def __init__(self):
        self.collection_name = ""
        self.collection_alias = ""
        self.dataverse_contacts = []
        self.affiliation = ""
        self.description = ""
        self.dataverse_type = ""
        self.collection_parent = ""

    def render(self):
        """
        Turn the collection into a json dict structure for transmission to dataverse
        :return:
        """
        template_processor = TemplateProcessor()
        template = template_processor.retrieve_template("dataverse-collection")
        return template.render(collection=self)

class DataverseDataset:
    """
    Represents a dataset
    """

    def __init__(self):
        self.protocol = ""
        self.authority = ""
        self.identifier = ""
        self.citation = CitationMetadataBlock()
        self.file = [] # see DatasetFile

    def render(self):
        """
        Turn the collection into a json string for transmission to dataverse
        :return: dict with json version of dataset
        """
        template_processor = TemplateProcessor()
        template = template_processor.retrieve_template("dataverse-extended")
        return template.render(dataset=self)

class DataverseDatasetLicense:
    """
    License in a dataset
    """

    def __init__(self, name, uri):
        self.name = name
        self.uri = uri

class CitationMetadataBlock:
    """
    Metadata block in a dataset
    """

    def __init__(self):
        self.display_name = "Citation Metadata"
        self.title = ""
        self.subtitle = ""
        self.alternative_title = ""
        self.alternative_url = ""
        self.other_id = ""
        self.other_id_agency = ""
        self.other_id_value = ""
        self.author = [] # see CitationAuthor
        self.dataset_contact = [] # see DatasetContact
        self.dataset_description = [] # see DatasetDescription
        self.subject = []
        self.keyword = [] # see DatasetKeyword
        self.topic_classification = [] # see TopicClassification
        self.publication = [] # see DatasetPublication
        self.notes_text = ""
        self.language = []
        self.producer = [] # see DatasetProducer
        self.production_date = ""
        self.production_place = ""
        self.contributor = []  # see Contributor
        self.grant = [] # see Grant
        self.distributor = [] # see Distributor
        self.distribution_date = ""
        self.date_of_deposit = ""
        self.time_period = [] # see TimePeriod
        self.date_of_collection = [] # see TimePeriod
        self.kind_of_data = []
        self.series = [] # Series
        self.software = [] # see Software
        self.related_material = []
        self.related_datasets = []
        self.other_references = []
        self.data_sources = []
        self.origin_of_sources = ""
        self.characteristics_of_sources_noted = ""


class CitationAuthor:
    """
    Citation in a metadata block
    """

    def __init__(self):
        self.author_name = ""
        self.author_affiliation = ""
        self.author_identifier_scheme = ""
        self.author_identifier = ""

class DatasetContact:
    """
    Dataset contact in metadata block
    """

    def __init__(self):
        self.contact_name = ""
        self.contact_affiliation = ""
        self.contact_email = ""

class DatasetDescription:
    """
    Dataset description
    """

    def __init__(self):
        self.description = ""
        self.description_date = ""

class DatasetKeyword:
    """
    Keyword in dataset
    """

    def __init__(self):
        self.keyword = ""
        self.keyword_uri = ""
        self.vocabulary = ""
        self.vocabulary_uri = ""

class TopicClassification:

    """
    Topic classification in a dataset
    """

    def __init__(self):
        self.topic_name = ""
        self.vocabulary = ""
        self.vocabulary_uri = ""


class Publication:

    """
    Publication in a dataset
    """

    def __init__(self):
        self.publication_relation_type = ""
        self.citation = ""
        self.id_type = ""
        self.id_number = ""
        self.url = ""

class Producer:

    """
    Producer of a dataset
    """

    def __init__(self):
        self.name = ""
        self.affiliation = ""
        self.abbreviation = ""
        self.url = ""
        self.logo_url = ""


class Contributor:
    """
    Contributor of a dataset
    """
    def __init__(self):
        self.type = ""
        self.name = ""

class Grant:
    """
    Grant of a dataset
    """

    def __init__(self):
        self.agency = ""
        self.number = ""

class Distributor:
    """
    Distributor of a dataset
    """

    def __init__(self):
        self.name = ""
        self.affiliation = ""
        self.abbreviation = ""
        self.url = ""
        self.logo_url = ""

class TimePeriod:
    """
    Time period of a dataset
    """
    def __init__(self):
        self.start = ""
        self.end = ""

class Series:
    """
    Series of a dataset
    """

    def __init__(self):
        self.name = ""
        self.information = ""

class Software:
    """
    Software block of a dataset
    """

    def __init__(self):
        self.name = ""
        self.version = ""

class DatasetFile:
    """
    File of a dataset
    """

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



