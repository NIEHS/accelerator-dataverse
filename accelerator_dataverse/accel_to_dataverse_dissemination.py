from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload
from accelerator_core.workflow.accel_target_dissemination import AccelDisseminationComponent

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
        """
        return dissemination_payload


