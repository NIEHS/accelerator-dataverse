import os
import unittest

from accelerator_core.services import dissemination
from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload, DisseminationDescriptor

from accelerator_dataverse.accel_to_dataverse_dissemination import AccelDataverseDissemination


class TestAccelToDataverseDissemination(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.api_key = os.environ["DATAVERSE_API_KEY"]
        cls.dataverse_host = os.environ["DATAVERSE_HOST"]

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ingest_single_inline(self):

        item_id = "test_ingest_single_inline_item"
        run_id = "test_ingest_single_inline_run"

        xcom_props_resolver = DirectXcomPropsResolver(temp_files_supported=False, temp_files_location=None)
        params = { 'api_key': self.__class__.api_key, 'run_id': run_id }

        disseminator = AccelDataverseDissemination(xcom_props_resolver)
        dissemination_descriptor = DisseminationDescriptor()
        dissemination_payload = DisseminationPayload(dissemination_descriptor)

        dissemination_payload = disseminator.disseminate(dissemination_payload, params)
        self.assertIsNotNone(dissemination_payload)

if __name__ == '__main__':
    unittest.main()
