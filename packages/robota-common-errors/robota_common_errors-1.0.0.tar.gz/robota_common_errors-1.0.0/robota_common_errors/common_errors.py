"""Common errors are suboptimal student behaviors that occur regularly. If a common error
is identified, feedback is given on how to correct it or avoid it in future.

Common errors are much like Tasks except they are not assigned any credit.
"""

import importlib
from loguru import logger
from typing import List

from robota_core import config_readers
from robota_core.config_readers import get_config, RobotaConfigParseError
from robota_core.string_processing import markdownify
from robota_core.data_server import DataServer


class CommonError:
    """Representation of a common error that could be identified

    :ivar name: The name of the common error.
    :ivar marking_function: The name of the function used to assess the common error.
    :ivar description: A textual description of the common error.
    :ivar detail_titles: Titles of a table to be printed on the marking report.
    :ivar error_details: Rows of a table to be printed on the marking report.
    """
    def __init__(self, common_error: dict):
        self.name = common_error["name"]
        self.marking_function = common_error["marking_function"]
        self.description = markdownify(common_error["text"])
        self.required_data_sources: List[str] = common_error["required_data_sources"]
        self.detail_titles: List[str] = []
        self.error_details: List[List[str]] = []

    def __getstate__(self) -> dict:
        return {"name": self.name,
                "detail_titles": self.detail_titles,
                "error_details": self.error_details}

    def add_feedback(self, feedback: List[List[str]]):
        self.error_details = feedback

    def add_feedback_titles(self, feedback_titles: List[str]):
        self.detail_titles = feedback_titles

    def count_errors(self) -> int:
        """Sum the occurrences of this error by checking error details."""
        if not self.error_details:
            return 0
        else:
            return len(self.error_details[0])


def assess_common_errors(data_source: DataServer,
                         common_errors: List[CommonError]) -> List[CommonError]:
    """Go through all of the possible common errors, running the assessment function for each
    one."""
    if common_errors is None:
        return []

    completed_errors = []

    logger.info("Begun assessment of common errors.")
    common_errors_module = importlib.import_module('robota_common_errors.common_error_functions')
    for error in common_errors:
        logger.info(f"Assessing common error {error.name}.")
        if validate_data_sources(data_source, error):
            marking_function = getattr(common_errors_module, error.marking_function, None)
            if marking_function:
                completed_errors.append(marking_function(data_source, error))
            else:
                logger.warning(f"Common error function '{error.marking_function}' specified in "
                               f"common error: '{error.name}' but not found in "
                               f"'common_error_functions.py'. RoboTA will not assess this error.")

    logger.success("Completed assessment of common errors.")
    return completed_errors


def validate_data_sources(data_source: DataServer, common_error: CommonError):
    """Check the data sources that are available from the DataServer."""
    valid_sources = data_source.get_valid_sources()
    for source in common_error.required_data_sources:
        if source not in valid_sources:
            logger.warning(f"Common error {common_error.name} cannot be assessed as it requires "
                           f"the data source {source} which has not been provided in the "
                           f"robota config file.")
            return False
    return True


def get_error_descriptions(robota_config: dict) -> List[CommonError]:
    """Get the textual description of common errors to identify."""
    common_error_source = config_readers.get_data_source_info(robota_config, "common_errors")
    if not common_error_source:
        raise KeyError(f"common_errors data source not found in robota config. Must specify a "
                       f"source of common errors.")

    if "file_name" in common_error_source:
        error_file = common_error_source["file_name"]
    else:
        raise RobotaConfigParseError("Could not find key 'file_name' in 'common_error' data type "
                                     "in RoboTA config.")

    logger.info(f"Getting error config from {error_file}")
    error_config = get_config([error_file], common_error_source)[0]
    if error_config is None:
        raise KeyError(f"Failed to load common errors from file {error_file}.")
    else:
        return [CommonError(error_info) for error_info in error_config]
