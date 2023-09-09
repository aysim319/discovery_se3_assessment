import json
import os.path

import click
from datetime import datetime
import json
from pathlib import Path

from utils.fetch_data import get_picture_of_day, get_cleaned_wiki_data

PROJECT_DIR = Path(__file__).resolve().parent


@click.command()
@click.option(
    "--date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="date to grab for Astronomy Picture of the Day with the format YYYY-mm-dd, default to today",
    default=datetime.now().strftime("%Y-%m-%d"),
)
@click.option("--output",
              type=click.Path(),
              default=f"{PROJECT_DIR}/out/apod-data.json",
              help="output file including path, default to <project>/src/out/YYYY-mm-dd-apod-data.json"
)
def get_apod_data(date, output):
    '''
    Return a json file with the response from APOD api from NASA and additional information from wikipedia.
    '''
    if date > datetime.now() or date < datetime.strptime("1995-06-16", "%Y-%m-%d"):
        print(f"Invalid date; select a date between 1995-06-16 to today ({datetime.now().strftime('%Y-%m-%d')}) inclusive")
        exit(1)
    if output[-5:] != ".json":
        print("WARNING file extension is not .json and will be ignored")

    date_str = date.strftime("%Y-%m-%d")
    response = get_picture_of_day(date=date_str)
    if response:
        data = response.json()
        links = get_cleaned_wiki_data(data)
        data["ext_links"] = links

        filepath = Path(output).parent
        filename = Path(output).resolve().stem
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if filename == "apod-data":
            filename = f"{date_str}-apod-data"

        with open(f"{filepath}/{filename}.json", "w") as f:
            f.write(json.dumps(data, indent=4))

if __name__ == "__main__":
    get_apod_data()
