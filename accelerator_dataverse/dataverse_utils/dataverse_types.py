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
        Turn the collection into a json dict structure for transmisstion to dataverse
        :return:
        """
        template_processor = TemplateProcessor()
        template = template_processor.retrieve_template("dataverse-collection")
        return template.render(collection=self)