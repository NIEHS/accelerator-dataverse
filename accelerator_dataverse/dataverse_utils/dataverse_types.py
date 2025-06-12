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

