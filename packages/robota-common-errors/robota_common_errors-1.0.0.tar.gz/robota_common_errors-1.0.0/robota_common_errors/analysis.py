"""An example of a simple data analysis script that might be run on the JSON output of
common_error_collection.py."""

import pathlib

import pandas as pd
import plotly.express as px


def read_json(file_path: pathlib.Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(file_path)
    return pd.read_json(file_path)


def main(file_name: str):
    file_path = pathlib.Path(file_name)
    data = read_json(file_path)
    data = data.drop(["course", "team_name", "detail_titles", "error_details"], axis=1)
    error_counts = data.groupby(["year", "error_name"]).aggregate(sum).reset_index()
    with open("output.html", 'w') as output_file:
        for error_name, group in error_counts.groupby('error_name'):
            fig = px.bar(group, x="year", y="num_occurrences", title=error_name)
            fig.update_xaxes(type='category')
            html = fig.to_html("output.html", include_plotlyjs='cdn', full_html=False,
                               default_width="50%", default_height="50%")
            output_file.write(html)


if __name__ == '__main__':
    main("data.json")
