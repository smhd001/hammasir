import html
import os
import re
from urllib.parse import urlencode

import pandas as pd
import requests
from tqdm import tqdm

tqdm.pandas()
data_set_path = os.path.join(
    os.path.dirname(__file__), "../data/processed/base_dataset.csv"
)
base_dataset = pd.read_csv(data_set_path)


headers = {"User-Agent": "Apidog/1.0.0 (https://apidog.com)"}


def get_about(employee_id):
    employee_id = urlencode({"employee_id": employee_id})
    response = requests.get(
        f"https://apigw.paziresh24.com/v1/providers?{employee_id}", headers=headers
    )
    data = response.json()
    print(data)
    if not data["providers"] or not data["providers"][0]["biography"]:
        return None
    data = data["providers"][0]["biography"]
    data = html.unescape(data)
    # delete html tags using regex
    data = re.sub(r"<.*?>", "", data)


base_dataset[["about"]].to_csv("../data/processed/about_dataset.csv")
