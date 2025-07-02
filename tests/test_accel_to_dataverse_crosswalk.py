import json
import os
import unittest
from pathlib import Path

from accelerator_core.utils.resource_utils import determine_resource_path, determine_test_resource_path
from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_data_models import IngestSourceDescriptor, IngestPayload, DisseminationDescriptor, \
    DisseminationPayload

from accelerator_dataverse.accel_to_dataverse_crosswalk import AccelToDataverseCrosswalk


class TestAccelToDataverseCrosswalk(unittest.TestCase):

    def test_crosswalk(self):

        dissemination_descriptor = DisseminationDescriptor()
        dissemination_descriptor.ingest_type = "accelerator"
        dissemination_descriptor.schema_version = "1.0.0"
        dissemination_descriptor.dissemination_type = "dataverse"
        dissemination_descriptor.dissemination_item_id = "foo"
        dissemination_descriptor.use_tempfiles = False
        dissemination_descriptor.dissemination_identifier = "runid1"

        payload = DisseminationPayload(dissemination_descriptor)

        #dir = Path(os.path.dirname(__file__)).parent
        #filename = os.path.join(dir, "/test_resources/example1.json")
        filename = "./test_resources/example1.json"
        xcom_props_resolver = DirectXcomPropsResolver(False, None)

        with open(filename) as json_data:
            d = json.load(json_data)
            payload.payload.append(d)
            payload.payload_inline = True
            crosswalk = AccelToDataverseCrosswalk(xcom_props_resolver)
            actual = crosswalk.transform(payload)
            self.assertIsNotNone(actual)


if __name__ == '__main__':
    unittest.main()
