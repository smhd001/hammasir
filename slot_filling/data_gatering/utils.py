import os
import re
import sys

module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)

from read_data import batched, fill_and_filter_tags, get_tokens_row_len  # noqa: E402


def tsv_to_list(text) -> list:
    data = []
    for i, (tokens, labels) in enumerate(batched(text.split("\n"), 2)):
        tokens = tokens.split()
        labels = labels.split()
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


def conll_to_list(text) -> list:
    data = []
    for i, row in enumerate(text.split("\n\n")):
        tokens = []
        labels = []
        for line in row.split("\n"):
            line = line.strip()
            if len(line) == 0:
                break
            token, label = line.split()
            tokens.append(token)
            labels.append(label)
        data.append(
            {
                "id": i,
                "tokens": tokens,
                "tags": labels,
            }
        )
    return data


def conll_to_tsv(text, sep="\t") -> str:
    ll = conll_to_list(text)
    result = ""
    for row in ll:
        result += sep.join(row["tokens"]) + "\n" + sep.join(row["tags"]) + "\n"
    return result


def tsv_to_conll(text, sep=" ") -> str:
    ll = tsv_to_list(text)
    result = ""
    for row in ll:
        result += "\n".join(
            [
                f"{row['tokens'][i]}{sep}{row['tags'][i]}"
                for i in range(len(row["tokens"]))
            ]
        )
        result += "\n\n"
    return result


def split_to_token(text: str) -> list:
    return re.split(r"[\b\W\b]+", text)
