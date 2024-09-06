import html
import json
import os
import re
import time
from urllib.parse import urlencode

import pandas as pd
import requests
from tqdm import tqdm

tqdm.pandas()
DATASET_DIR = os.path.join(os.path.dirname(__file__), "../data/processed")
base_dataset = pd.read_csv(DATASET_DIR + "/base_dataset.csv")


headers = {"User-Agent": "Apidog/1.0.0 (https://apidog.com)"}


def get_about(employee_id):
    employee_id = urlencode({"employee_id": employee_id})
    retries = 3
    for _ in range(retries):
        try:
            response = requests.get(
                f"https://apigw.paziresh24.com/v1/providers?{employee_id}",
                headers=headers,
            )
            data = response.json()
            break
        except json.decoder.JSONDecodeError:
            time.sleep(1)
            data = None

    print(data)
    if not data or not data["providers"] or not data["providers"][0]["biography"]:
        return None
    data = data["providers"][0]["biography"]
    data = html.unescape(data)
    # delete html tags using regex
    data = re.sub(r"<.*?>", "", data)
    return data


NUM_PARTITIONS = 10
for i in range(NUM_PARTITIONS):
    print(f"Partition {i}")
    partition = base_dataset[
        i * len(base_dataset) // NUM_PARTITIONS : (i + 1)
        * len(base_dataset)
        // NUM_PARTITIONS
    ]
    partition["about"] = partition["medical_code"].progress_apply(get_about)
    print(partition[["about"]])
    partition[["about"]].to_csv(DATASET_DIR + f"/about_dataset_{i}.csv")

NUM_PARTITIONS = 10
about = pd.concat(
    [
        pd.read_csv(DATASET_DIR + f"/about_dataset_{i}.csv", index_col=0)
        for i in range(NUM_PARTITIONS)
    ]
)
about.to_csv(DATASET_DIR + "/about_dataset.csv")
