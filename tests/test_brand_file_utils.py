import unittest

from accelerator_dataverse.dataverse_utils.brand_file_utils import determine_brand_file_path


class TestBrandFileUtils(unittest.TestCase):
    def test_determine_brand_file_path(self):
        actual = determine_brand_file_path()
        self.assertIsNotNone(actual)

if __name__ == '__main__':
    unittest.main()
