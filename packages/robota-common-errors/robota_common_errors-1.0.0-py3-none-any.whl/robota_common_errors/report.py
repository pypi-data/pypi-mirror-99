"""Generates a HTML report of common errors for a git repo."""
import argparse
import datetime
from loguru import logger
import os
import pathlib
from typing import List

import dateutil.parser
import jinja2

import robota_core.config_readers as config_readers
from robota_core.data_server import DataServer

from robota_common_errors.common_errors import get_error_descriptions, CommonError
from robota_common_errors.common_errors import assess_common_errors
from robota_common_errors.output_templates.build_webpages import build_webpages


def count_errors(common_errors: List[CommonError]) -> int:
    """Count how many different common error types were detected."""
    error_count = 0
    for error in common_errors:
        if error.detail_titles:
            error_count += 1
    return error_count


def identify_common_errors(robota_config: dict, start: datetime.datetime,
                           end: datetime.datetime) -> List[CommonError]:
    """The main function which gets the common errors."""
    # Set up data source
    data_server = DataServer(robota_config, start, end)

    # Obtain info on common errors from YAML files
    common_errors = get_error_descriptions(robota_config)

    # Identify common errors.
    return assess_common_errors(data_server, common_errors)


def output_html_report(common_errors: List[CommonError], data_source_info: dict,
                       common_error_summary: dict, output_dir: str):

    # Construct the marking report based on determined performance
    update_template(common_errors, data_source_info, common_error_summary)

    # Build the webpages copying from templates to the live directory
    template_dir = pathlib.Path(__file__).parent / "output_templates"
    build_webpages(template_dir, pathlib.Path(output_dir))


def update_template(common_errors: List[CommonError], data_source_info: dict,
                    common_error_summary: dict):
    """Produce the HTML report by writing the marking results to a HTML template.
    :param common_errors: A list of common errors and feedback on them.
    :param data_source_info: A dictionary of information about the data sources that were used.
    :param common_error_summary: A dictionary of stats about the common errors that is printed in
        the report.
    """
    logger.info("Writing common error report.")
    template_loader = jinja2.FileSystemLoader(
        searchpath=f"robota_common_errors/output_templates/")
    template_env = jinja2.Environment(loader=template_loader, trim_blocks=True,
                                      lstrip_blocks=True,
                                      undefined=jinja2.StrictUndefined)

    jinja_template = template_env.get_template("common_error_report/report_template.html")

    rendered_page = jinja_template.render(common_errors=common_errors,
                                          common_error_summary=common_error_summary,
                                          data_source_info=data_source_info)

    # prepare the output directory
    output_directory = pathlib.Path("webpages/").resolve()
    os.makedirs(output_directory, exist_ok=True)

    # Write the generated report to a file
    output_name = "common-error-report.html"
    report_path = output_directory / pathlib.Path(output_name)
    with open(report_path, "w", encoding='utf-8') as result_html:
        result_html.write(rendered_page)
    logger.info("Common error report complete.")


def summarise_data_sources(robota_config: dict, start: datetime.datetime,
                           end: datetime.datetime) -> dict:
    data_source_summary = {"start": start, "end": end}
    desired_sources = ["issues", "remote_provider", "repository", "ci"]
    for source in desired_sources:
        source_info = config_readers.get_data_source_info(robota_config, source)
        if source_info:
            source_info.pop("token", None)
            source_info.pop("username", None)
            data_source_summary[source] = source_info
    return data_source_summary


def summarise_common_errors(common_errors: List[CommonError]):
    error_summary = {"num_tested_errors": len(common_errors),
                     "num_detected_errors": 0}
    for error in common_errors:
        if error.count_errors() > 1:
            error_summary["num_detected_errors"] += 1
    return error_summary


def run_html_error_report(start: str, end: str, config_path: str, output_dir: str,
                          substitution_variables: dict):
    """Get common errors and output them in the form of a HTML report."""
    start = dateutil.parser.parse(start)
    end = dateutil.parser.parse(end)
    # Get robota config from local config file
    robota_config = config_readers.get_robota_config(config_path, substitution_variables)
    common_errors = identify_common_errors(robota_config, start, end)
    data_source_info = summarise_data_sources(robota_config, start, end)
    common_error_summary = summarise_common_errors(common_errors)
    output_html_report(common_errors, data_source_info, common_error_summary, output_dir)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config_path",
                        help="The path to the robota-config.yaml file.",
                        default="robota-config.yaml")
    parser.add_argument("-o", "--output_dir",
                        help="The output directory to place the report.",
                        default="webpages/")
    parser.add_argument("-s", "--start",
                        help="The start date of the first commit to consider in YYYY-MM-DD format.",
                        default="2020-01-01")
    parser.add_argument("-e", "--end",
                        help="The end date of the last commit to consider in YYYY-MM-DD format.",
                        default=datetime.date.today().isoformat())

    parsed, unknown_args = parser.parse_known_args()
    KNOWN_ARGS = vars(parsed)

    if len(unknown_args) % 2 != 0:
        raise SyntaxError("Malformed command line arguments. "
                          "Each flag must be followed by a single argument.")
    while unknown_args:
        flag = unknown_args.pop(0).lstrip("-")
        value = unknown_args.pop(0)
        KNOWN_ARGS[flag] = value

    run_html_error_report(KNOWN_ARGS.pop("start"), KNOWN_ARGS.pop("end"),
                          KNOWN_ARGS.pop("config_path"), KNOWN_ARGS.pop("output_dir"),
                          KNOWN_ARGS)
