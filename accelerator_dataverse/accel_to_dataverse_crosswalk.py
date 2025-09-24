import json

from accelerator_core.schema.models.accel_model import AccelDataResourceModel
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import IngestPayload, DisseminationPayload
from accelerator_core.workflow.crosswalk import Crosswalk
from accelerator_core.utils.data_utils import from_dict, to_dict
from accelerator_core.workflow.dissemination_crosswalk import DisseminationCrosswalk

from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseDataset, DatasetKeyword, Publication, \
    Producer, TimePeriod, DatasetDescription, GeospatialMetadataBlock, GeographicBoundingBox, CitationAuthor, \
    TopicClassification, DatasetContact, DataverseCafeSourceDataset

logger = setup_logger("accelerator-dataverse")

class AccelToDataverseCrosswalk(DisseminationCrosswalk):
    """
    Crosswalk from accelerator to dataverse
    Version 1.0.0
    """

    def __init__(self, xcom_props_resolver:XcomPropsResolver):
        """
        Constructor takes xcom_props_resolver as an XcomPropsResolver.
        :param xcom_props_resolver: XcomPropsResolver
        """
        super().__init__(xcom_props_resolver)

    def transform(self, payload: DisseminationPayload) -> DisseminationPayload:
        """
        Convert accel format data to dataverse format.
        :param ingest_result: IngestPayload coming from accelerator
        :return: IngestPayload containing dataverse data
        """

        logger.info(f"transforming: {payload}")

        payload_length = self.get_payload_length(payload)

        if payload_length > 1:
            raise NotImplementedError("multiple payload entries not supported")

        payload_entry = self.payload_resolve(payload,0)
        logger.debug(f"payload_entry: {payload_entry}")

        dataset = DataverseDataset()
        # TODO: add license data, shim out for now
        dataset.license.name = "CC0 1.0"
        dataset.license.url = "http://creativecommons.org/licenses/by/2.0/"

        logger.info(f"payload entry: {payload_entry}")

        data = payload_entry['data']
        accel_geospatial_data = data['geospatial_data']
        accel_project_data = data["project"]
        accel_data_resource = data["data_resource"]
        accel_resource = data["resource"]
        accel_data_usage = data["data_usage"]
        accel_computational_workflow = data["computational_workflow"]

        citation = dataset.citation
        citation.title = accel_resource["resource_name"]
        citation.alternative_url = accel_resource["resource_url"]
        citation.depositor = payload_entry["submission"]["submitter_name"]

        for sponsor in accel_project_data["project_sponsor"]:
            citation_author = CitationAuthor()

            if sponsor["name"]:
                citation_author.author_name = sponsor["name"]
            else:
                citation_author.author_name = sponsor["type"]

            citation.author.append(citation_author)

        for sponsor in accel_project_data["project_sponsor"]:
            dataset_contact = DatasetContact()

            if sponsor["name"]:
                dataset_contact.contact_name = sponsor["name"]
            else:
                dataset_contact.contact_name = sponsor["type"]

            dataset_contact.contact_email = "noreply@chordshealth.org" # TODO: temp shim mc

            citation.dataset_contact.append(dataset_contact)

        dataset_description = DatasetDescription()
        dataset_description.description = accel_resource["resource_description"]

        citation.dataset_description.append(dataset_description)

        citation.subject.append("Medicine, Health and Life Sciences")
        citation.subject.append("Earth and Environmental Sciences")

        for keyword in accel_resource["resource_keywords"]:
            ds_key = DatasetKeyword()
            ds_key.keyword = keyword
            citation.keyword.append(ds_key)

        for publication in accel_resource["publication"]:
            ds_publication = Publication()
            ds_publication.publication_relation_type = "Cites"
            ds_publication.citation = publication["citation"]
            ds_publication.url = publication["citation_link"]
            ds_publication.id_type = "url"
            citation.publication.append(ds_publication)

            citation.notes_text = accel_resource["resource_description"]

        producer = Producer()
        producer.name = accel_project_data["project_name"]
        producer.abbreviation = accel_project_data["project_short_name"]
        producer.url = accel_project_data["project_url"]

        citation.producer.append(producer)

        time_start = accel_data_resource["time_extent_start"]
        time_end = accel_data_resource["time_extent_end"]

        if time_start or time_end:
            time_period = TimePeriod()
            time_period.start = f"{time_start}-01-01"
            time_period.end = f"{time_end}-12-31"
            citation.time_period.append(time_period)

        # data_resource

        for measure in accel_data_resource["measures"]:
            topic = TopicClassification()
            topic.topic_name = measure["value"]
            citation.topic_classification.append(topic)

        for item in accel_data_resource["data_location"]:

            text = item["data_location_text"]
            link = item["data_location_link"]

            if text:
                citation.related_datasets.append(text)

            if link:
                citation.related_datasets.append(link)

        dataverse_geospatial_data = GeospatialMetadataBlock()

        if accel_geospatial_data["spatial_bounding_box"]:
            if len(accel_geospatial_data.spatial_bounding_box) != 4:
                raise Exception("spatial_bounding_box must be a list of 4 floats")
            else:
                bounding_box = GeographicBoundingBox()
                bounding_box.south = accel_geospatial_data.spatial_bounding_box[0]
                bounding_box.west = accel_geospatial_data.spatial_bounding_box[1]
                bounding_box.north = accel_geospatial_data.spatial_bounding_box[2]
                bounding_box.east = accel_geospatial_data.spatial_bounding_box[3]
                dataverse_geospatial_data.geographic_bounding_box = bounding_box

        for publication in accel_resource["publication"]:
            ds_publication = Publication()
            ds_publication.publication_relation_type = "Cites"
            ds_publication.citation = publication["citation"]
            ds_publication.url = publication["citation_link"]
            ds_publication.id_type = "url"
            citation.publication.append(ds_publication)

        citation.notes_text = accel_resource["resource_description"]
        citation.kind_of_data.append(accel_resource["resource_type"])

        for item in accel_resource["resource_reference"]:
            text = item["resource_reference_text"]
            link = item["resource_reference_link"]

            if text:
                citation.related_material.append(text)

            if link:
                citation.related_material.append(link)

        # cafe custom metadata items

        # TODO: refine data type in accel core?

        if accel_resource["resource_type"] == "Data Resource":
            dataset.cafe_custom.includes_geospatial_file = "Yes"
        else:
            dataset.cafe_custom.includes_geospatial_file = "No"

        dataset.cafe_custom.derived_from_existing_dataset = "Yes"

        # CAFE dataset metadata

        for item in accel_data_resource["data_location"]:

            cafe_dataset = DataverseCafeSourceDataset()
            cafe_dataset.title = item["data_location_text"]
            cafe_dataset.doi_or_url = item["data_location_link"]
            cafe_dataset.institution = producer.name
            dataset.cafe_custom.source_data.append(cafe_dataset)

        # combine multiple items into the notes field
        notes_field = ""
        if accel_data_usage["intended_use"]:
            notes_field += AccelToDataverseCrosswalk.listit("Intended Use", accel_data_usage["intended_use"]["value"])
            notes_field += "<br/>"

        if accel_data_usage["strengths"]:
            notes_field += AccelToDataverseCrosswalk.listit("Strengths", accel_data_usage["strengths"])
            notes_field += "<br/>"

        if accel_data_usage["limitations"]:
            notes_field += AccelToDataverseCrosswalk.listit("Limitations", accel_data_usage["limitations"])
            notes_field += "<br/>"

        if accel_data_usage["suggested_audience"]:
            notes_field += AccelToDataverseCrosswalk.listit("Suggested Audience", accel_data_usage["suggested_audience"])
            notes_field += "<br/>"

        if accel_computational_workflow["use_tools"]:
            notes_field += AccelToDataverseCrosswalk.listit("Use Tool", accel_computational_workflow["use_tools"])
            notes_field += "<br/>"

        if accel_computational_workflow["example_applications"]:
            notes_field += AccelToDataverseCrosswalk.listit("Example Application", accel_computational_workflow["example_applications"])
            notes_field += "<br/>"

        citation.notes_text = notes_field

        for data_format in accel_data_resource["data_formats"]:
            citation.kind_of_data.append(data_format)



        rendered = dataset.render()
        dataverse_data = json.loads(rendered)

        return_payload = DisseminationPayload(payload.dissemination_descriptor)
        self.report_individual_dissemination(return_payload, "itemid", dataverse_data)
        logger.debug(f"return payload from crosswalk: {return_payload}")

        return return_payload

    @staticmethod
    def boldit(val:str) -> str:
        return f"<b>{val}</b>"

    @staticmethod
    def listit(heading:str, val:[str]) -> str:
        ul = "<ul>"
        ul_end = "</ul>"
        li = "<li>"
        li_end = "</li>"
        retval = AccelToDataverseCrosswalk.boldit(heading)
        retval += ul
        for item in val:
            retval += f"{li}{item}{li_end}"
        retval += ul_end
        return retval







