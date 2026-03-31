import logging

from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload
from accelerator_core.workflow.accel_target_dissemination import AccelDisseminationComponent

from accelerator_dataverse.dataverse_utils.dataverse_config import DataverseConfig
from accelerator_dataverse.dataverse_utils.dataverse_connector import DataverseConnector

logger = logging.getLogger(__name__)

class AccelDataverseDissemination(AccelDisseminationComponent):
    """
    Disseminator of accelerator data to dataverse
    """

    def __init__(self, xcom_props_resolver:XcomPropsResolver):
        super().__init__(xcom_props_resolver)

    def disseminate(
        self, dissemination_payload: DisseminationPayload, additional_parameters=None
    ) -> DisseminationPayload:
        """
        Disseminate the incoming payload out to Dataverse
        :param dissemination_payload: DisseminationPayload with information about the dissemination along
        with the actual payload data
        :param additional_parameters: dict with additional parameters particular to this task
        :return: DisseminationPayload with information about the dissemination result

        required additional parameters:

        dataverse_host: Dataverse host
        dataverse: Dataverse collection
        api_key: Dataverse API key

        optional additional parameters:

        accel_data_file: string with the absolute path to a sidecar file containing the accelerator data model, if
        present this will be uploaded to the dataverse

        """
        if additional_parameters is None:
            additional_parameters = {}
        logger.info(f"disseminate with descriptor {dissemination_payload.dissemination_descriptor}")
        dataverse_config = DataverseConfig(dataverse_host=additional_parameters["dataverse_host"],
                                           api_key=additional_parameters["api_key"],
                                           dataverse=additional_parameters["dataverse"],)

        dataverse_connector = DataverseConnector(dataverse_config)

        payload_length = self.get_payload_length(dissemination_payload)

        # right now we are supporting single payloads

        if payload_length > 1:
            raise NotImplementedError(f"dissemination payload length {payload_length} > 1")

        if payload_length == 0:
            logger.warning(f"dissemination payload length {payload_length} > 0, no work to do")
            return dissemination_payload

        payload_doc = self.payload_resolve(dissemination_payload, 0)
        logger.debug(f"payload doc {payload_doc}")

        # TODO: make result share any error msgs (make a structure) and pass back in descriptor
        result = dataverse_connector.create_dataset_from_dict(dataverse_config.dataverse, payload_doc)
        logger.info(f"created dataset from dict - result:{result}")

        doi = result.pid
        logger.info(f"doi: {doi}")

        logger.info("looking for additional files to upload to dataverse")

        if additional_parameters:
            accel_data_file = additional_parameters.get("accel_data_file")

            if accel_data_file:
                logger.info(f"uploading acceldata file {accel_data_file} to dataverse")
                dataverse_connector.add_file_to_dataverse(doi, accel_data_file)


        dissemination_payload.dissemination_successful = True
        dissemination_payload.payload_inline = True
        dissemination_payload.payload = []
        dissemination_payload.payload.append(result.to_dict())

        if additional_parameters.get("accel_data_model"):
            logger.info(f"storing accel data model in dataverse")

        return dissemination_payload


