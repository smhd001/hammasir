import os

import config
from utils import conll_to_tsv


def merge_data():
    files = {}
    for source in ["human", "gpt"]:
        dir_file = os.listdir(config.LABELING_DIR_PATH + "/" + source)
        files[source] = [
            config.LABELING_DIR_PATH + "/" + source + "/" + file for file in dir_file
        ]
    for file in files["human"]:
        data = open(file, "r").read()
        if data[-1] != "\n":
            data += "\n"
        open(config.MERGED_FILE_PATH, "a").write(data)

    for file in files["gpt"]:
        data = open(file, "r").read()
        if data[-1] != "\n":
            data += "\n"
        conll = open(file, "r").read()
        open(config.MERGED_FILE_PATH, "a").write(conll_to_tsv(conll, sep=","))


if __name__ == "__main__":
    merge_data()
