# This script aims to iterate over many gitlab repositories to collect data about the common
# errors made by students.
import argparse
import pathlib
from dataclasses import dataclass
from typing import List

from tqdm import tqdm
import jsonpickle
import yaml

from robota_common_errors.report import identify_common_errors
from robota_core import config_readers


@dataclass
class CommonErrorReport:
    course: str
    year: str
    team_name: str
    error_name: str
    detail_titles: List[str]
    error_details: List[List[str]]
    num_occurrences: int


def main(config_path: str, output_name: str):
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    output_path = pathlib.Path(output_name)
    try:
        output_path.unlink()
    except FileNotFoundError:
        pass

    error_list: List[CommonErrorReport] = []
    for variable_set in tqdm(config["variable_substitutions"], desc="Variable set"):
        max_team_number = variable_set["max_team_number"]
        if "min_team_number" in variable_set:
            min_team_number = variable_set["min_team_number"]
        else:
            min_team_number = 1
        for team_number in tqdm(range(min_team_number, max_team_number + 1), desc="Team number"):
            course = variable_set["course"]
            year = variable_set["year"]
            # Set up data source
            substitution_dict = {"year": str(year), "team": f"S1Team{team_number:02d}"}

            robota_config = config_readers.get_robota_config(config_path, substitution_dict)

            # Identify common errors.
            common_errors = identify_common_errors(robota_config, variable_set["start"],
                                                   variable_set["end"])
            for error in common_errors:
                error_list.append(CommonErrorReport(course, year, team_number, error.name,
                                                    error.detail_titles, error.error_details,
                                                    error.count_errors()))

    output_to_json(output_name, error_list)


def output_to_json(file_name: str, common_error_reports: List[CommonErrorReport]):
    with open(file_name, 'a') as output_file:
        output_file.write(jsonpickle.encode(common_error_reports, unpicklable=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--robota_config",
                        help="The location of the robota_config file",
                        default='robota-looping-config.yaml',
                        type=str)
    parser.add_argument("-o", "--output",
                        help="Where to output the data.",
                        default='data.json',
                        type=str)

    args = vars(parser.parse_args())

    main(args["robota_config"], args["output"])
