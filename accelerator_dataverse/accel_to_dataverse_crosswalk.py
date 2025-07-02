import json

from accelerator_core.schema.models.accel_model import AccelDataResourceModel
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import IngestPayload, DisseminationPayload
from accelerator_core.workflow.crosswalk import Crosswalk
from accelerator_core.utils.data_utils import from_dict, to_dict
from accelerator_core.workflow.dissemination_crosswalk import DisseminationCrosswalk

from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseDataset, DatasetKeyword, Publication, \
    Producer, TimePeriod, DatasetDescription

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

        citation = dataset.citation
        citation.title = data["resource"]["resource_name"]
        citation.alternative_url = data["resource"]["resource_url"]
        citation.depositor = payload_entry["submission"]["submitter_name"]

        dataset_description = DatasetDescription()
        dataset_description.description = data["resource"]["resource_description"]

        citation.dataset_description.append(dataset_description)
        citation.subject.append("Medicine, Health and Life Sciences")

        for keyword in data["resource"]["resource_keywords"]:
            ds_key = DatasetKeyword()
            ds_key.keyword = keyword
            citation.keyword.append(ds_key)

        for publication in data["resource"]["publication"]:
            ds_publication = Publication()
            ds_publication.publication_relation_type = "Cites"
            ds_publication.citation = publication["citation"]
            ds_publication.url = publication["citation_link"]
            ds_publication.id_type = "url"
            citation.publication.append(ds_publication)

            citation.notes_text = data["resource"]["resource_description"]

        producer = Producer()
        producer.name = data["project"]["project_name"]
        producer.abbreviation = data["project"]["project_short_name"]
        producer.url = data["project"]["project_url"]

        citation.producer.append(producer)

        #contributor?

        time_start = data["data_resource"]["time_extent_start"]
        time_end = data["data_resource"]["time_extent_end"]

        if time_start or time_end:
            time_period = TimePeriod()
            time_period.start = time_start
            time_period.end = time_end
            citation.time_period.append(time_period)

        # <data

        # data_resource

        #license = dataset.license
        #license.name = ""

        # geospatial_data

        # population_data

        # program

        # project

        # resource

        # temporal_data

        # <submission

        # <technical_metadata

        dataverse_data = json.loads(dataset.render())

        return_payload = DisseminationPayload(payload.dissemination_descriptor)
        self.report_individual_dissemination(return_payload, "itemid", dataverse_data)
        logger.debug(f"return payload from crosswalk: {return_payload}")

        return return_payload











