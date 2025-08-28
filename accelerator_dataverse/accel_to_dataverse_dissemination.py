from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload
from accelerator_core.workflow.accel_target_dissemination import AccelDisseminationComponent

from accelerator_dataverse.dataverse_utils.dataverse_config import DataverseConfig
from accelerator_dataverse.dataverse_utils.dataverse_connector import DataverseConnector
from accelerator_dataverse.dataverse_utils.dataverse_types import DataverseDataset

logger = setup_logger("accelerator")


class AccelDataverseDissemination(AccelDisseminationComponent):
    """
    Disseminator of accelerator data to dataverse
    """

    def __init__(self, xcom_props_resolver:XcomPropsResolver):
        super().__init__(xcom_props_resolver)

    def disseminate(
        self, dissemination_payload: DisseminationPayload, additional_parameters: dict
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

        """
        logger.info(f"disseminate with descriptor {dissemination_payload.dissemination_descriptor}")
        dataverse_config = DataverseConfig(dataverse_host=additional_parameters["dataverse_host"],
                                           api_key=additional_parameters["api_key"],
                                           dataverse=additional_parameters["dataverse"])

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
        logger.info(f"result:{result}")
        dissemination_payload.dissemination_successful = result
        if not result:
            raise Exception("dissemination failed, see log for errors")

        return dissemination_payload


