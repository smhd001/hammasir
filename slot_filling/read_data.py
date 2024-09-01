import csv
from itertools import islice

all_tag_names = [
    "problem",
    "city",
    "expertise",
    "gender",
    "neighborhood",
    "online-or-in-person",
    "insurance",
    "first-available-appointment",
    "amount-of-delay",
    "moral",
    "user-score",
    "experience",
]
selected_tag_names = [
    "problem",
    "city",
    "expertise",
    "gender",
]
NOLABEL = "O"
tags_list = []
for name in selected_tag_names:
    tags_list.extend([f"B-{name}", f"I-{name}"])
tags_list.append(NOLABEL)

all_tags_list = []
for name in selected_tag_names:
    all_tags_list.extend([f"B-{name}", f"I-{name}"])
all_tags_list.append(NOLABEL)


def batched(iterable, n):
    """batched('ABCDEFG', 3) → ABC DEF G"""
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


def get_tokens_row_len(row):
    i = 0
    for t in row:
        if t == "":
            break
        i += 1
    return i


def fill_and_filter_tags(labels):
    for i in range(len(labels)):
        if labels[i] not in tags_list:
            labels[i] = NOLABEL
    return labels


def read_data(file_path: str) -> dict:
    data = []
    with open(file_path, newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, (tokens, labels) in enumerate(batched(csv_reader, 2)):
            row_len = get_tokens_row_len(tokens)
            if row_len == 0:
                break
            data.append(
                {
                    "id": i,
                    "tokens": tokens[:row_len],
                    "tags": fill_and_filter_tags(labels[:row_len]),
                }
            )
    return data


def print_data(data: list[dict]) -> None:
    max_token_len = 30
    for row in data:
        print(row["id"])
        print(" ".join(r.rjust(max_token_len) for r in row["tokens"]))
        print(" ".join(r.rjust(max_token_len) for r in row["tags"]))
