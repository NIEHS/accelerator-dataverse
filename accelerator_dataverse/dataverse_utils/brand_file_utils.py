
import logging

from accelerator_core.utils.resource_utils import determine_resource_path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(filename)s:%(funcName)s:%(lineno)d: %(message)s"

)

logger = logging.getLogger(__name__)

def determine_brand_file_path():
    brand_file_path = determine_resource_path("accelerator_dataverse.dataverse_utils.templates", "README.md")
    if not brand_file_path.exists():
        raise FileNotFoundError(f"Could not find brand file at {brand_file_path}")

    logger.info(f"Brand file found at {brand_file_path}")
    return brand_file_path

