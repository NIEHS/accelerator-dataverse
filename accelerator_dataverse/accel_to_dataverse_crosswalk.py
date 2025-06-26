import json

from accelerator_core.schema.models.accel_model import AccelDataResourceModel
from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import IngestPayload, DisseminationPayload
from accelerator_core.workflow.crosswalk import Crosswalk
from accelerator_core.utils.data_utils import from_dict, to_dict
from accelerator_core.workflow.dissemination_crosswalk import DisseminationCrosswalk

from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseDataset

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

        dataset = DataverseDataset()
        # TODO: add license data, shim out for now
        dataset.license.name = "CC0 1.0"
        dataset.license.url = "http://creativecommons.org/licenses/by/2.0/"

        data = payload_entry['data']

        logger.info(f"payload entry: {payload_entry}")

        citation = dataset.citation
        citation.display_name = data["resource"]["resource_name"]

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











