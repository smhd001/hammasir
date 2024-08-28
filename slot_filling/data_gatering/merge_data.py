import os

import config


def merge_data():
    files = []
    for source in ["human", "gpt"]:
        dir_file = os.listdir(config.LABELING_DIR_PATH + "/" + source)
        files.extend(
            [config.LABELING_DIR_PATH + "/" + source + "/" + file for file in dir_file]
        )
    for file in files:
        print(file)
        open(config.MERGED_FILE_PATH, "a").write(open(file, "r").read())


if __name__ == "__main__":
    merge_data()
