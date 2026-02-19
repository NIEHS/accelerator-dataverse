import json
import os
import unittest

from accelerator_core.services import dissemination
from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload, DisseminationDescriptor

from accelerator_dataverse.accel_to_dataverse_crosswalk import AccelToDataverseCrosswalk
from accelerator_dataverse.accel_to_dataverse_dissemination import AccelDataverseDissemination


class TestAccelToDataverseDissemination(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.api_key = os.environ["DATAVERSE_API_KEY"]
        cls.dataverse_host = os.environ["DATAVERSE_HOST"]
        cls.dataverse = os.environ["DATAVERSE"]

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ingest_single_key_dataset_inline(self):

        item_id = "test_ingest_single_inline_item"
        run_id = "test_ingest_single_inline_run"

        dissemination_descriptor = DisseminationDescriptor()
        dissemination_descriptor.ingest_type = "accelerator"
        dissemination_descriptor.schema_version = "1.0.2"
        dissemination_descriptor.dissemination_type = "dataverse"
        dissemination_descriptor.dissemination_item_id = "foo"
        dissemination_descriptor.use_tempfiles = False
        dissemination_descriptor.dissemination_identifier = "runid1"

        payload = DisseminationPayload(dissemination_descriptor)

        filename = "./test_resources/example1.json"
        xcom_props_resolver = DirectXcomPropsResolver(False, None)

        params = {"api_key": self.__class__.api_key, "dataverse_host": self.__class__.dataverse_host, "run_id": run_id, "dataverse": self.__class__.dataverse}

        with open(filename) as json_data:
            d = json.load(json_data)
            payload.payload.append(d)
            payload.payload_inline = True
            crosswalk = AccelToDataverseCrosswalk(xcom_props_resolver)
            transformed = crosswalk.transform(payload)
            disseminator = AccelDataverseDissemination(xcom_props_resolver)
            dissemination_payload = disseminator.disseminate(transformed, params)
            self.assertIsNotNone(dissemination_payload)

    def test_ingest_single_geospatial_inline(self):

        item_id = "test_ingest_single_geospatial_inline"
        run_id = "test_ingest_single_inline_run"

        dissemination_descriptor = DisseminationDescriptor()
        dissemination_descriptor.ingest_type = "accelerator"
        dissemination_descriptor.schema_version = "1.0.2"
        dissemination_descriptor.dissemination_type = "dataverse"
        dissemination_descriptor.dissemination_item_id = "foo"
        dissemination_descriptor.use_tempfiles = False
        dissemination_descriptor.dissemination_identifier = "runid2"

        payload = DisseminationPayload(dissemination_descriptor)

        filename = "./test_resources/geospatial1.json"
        xcom_props_resolver = DirectXcomPropsResolver(False, None)

        params = {"api_key": self.__class__.api_key, "dataverse_host": self.__class__.dataverse_host, "run_id": run_id, "dataverse": self.__class__.dataverse}

        with open(filename) as json_data:
            d = json.load(json_data)
            payload.payload.append(d)
            payload.payload_inline = True
            crosswalk = AccelToDataverseCrosswalk(xcom_props_resolver)
            transformed = crosswalk.transform(payload)
            disseminator = AccelDataverseDissemination(xcom_props_resolver)
            dissemination_payload = disseminator.disseminate(transformed, params)
            self.assertIsNotNone(dissemination_payload)

if __name__ == '__main__':
    unittest.main()
