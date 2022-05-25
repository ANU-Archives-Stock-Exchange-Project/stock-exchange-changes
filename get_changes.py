import requests
from pathlib import Path
import json

JSON_URL = 'https://datasette.glamworkbench.cloud.edu.au/stock_exchange/stocks.json?edit_date__notblank=1&_shape=array'

def harvest_changes(url):
    rows = []
    while url:
        response = requests.get(url)
        try:
            url = response.links.get("next").get("url")
        except AttributeError:
            url = None
        rows.append(response.json())
    return rows

def main():
    Path('data').mkdir(exist_ok=True)
    rows = harvest_changes(JSON_URL)
    with Path('data', 'changes.json').open('w') as json_file:
        json.dump(rows, json_file, indent=2)

if __name__ == "__main__":
    main()