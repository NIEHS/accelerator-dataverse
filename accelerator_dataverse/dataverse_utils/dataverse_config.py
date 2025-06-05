from accelerator_core.utils.accelerator_config import AcceleratorConfig


class DataverseConfig:
    """
    Accelerator configuration for Dataverse
    """

    def __init__(self, dataverse_host:str, api_key:str):
        self.dataverse_host = dataverse_host
        self.api_key = api_key

