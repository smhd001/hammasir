import ast
from copy import deepcopy

import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "hammasir"),
    verify_certs=False,
    ssl_show_warn=False,
)
print(es.info())


def safe_literal_eval(val):
    try:
        if isinstance(val, str):
            return ast.literal_eval(val)
        else:
            return val  # If it's not a string, return the original value
    except (ValueError, SyntaxError):
        # Return None or a default value if evaluation fails
        return None


mappings = {
    "properties": {
        "gender": {"type": "keyword"},
        "expertise": {"type": "text"},
        "title": {"type": "text"},
        "star": {"type": "float"},
        "rates_count": {"type": "integer"},
        "number_of_visits": {"type": "integer"},
        "view": {"type": "text"},
        "insurances": {"type": "text"},
        "experience": {"type": "integer"},
        "doctor_encounter": {"type": "float"},
        "explanation_of_issue": {"type": "float"},
        "quality_of_treatment": {"type": "float"},
        "comments_count": {"type": "integer"},
        "waiting_time": {"type": "float"},
        "clinic": {"type": "object"},
        "medical_code": {"type": "text"},
        "about": {
            "type": "text",
        },
        "url": {"type": "text", "index": False},
        "image": {"type": "text", "index": False},
        "presence_freeturn": {"type": "date", "format": "epoch_second"},
    }
}


# because we uses synonyms we have to set serrate index and search time analyzer
# see https://www.elastic.co/blog/boosting-the-power-of-elasticsearch-with-synonyms for more details
persian_index_analyzer = {
    "tokenizer": "standard",
    "char_filter": ["zero_width_spaces"],
    "filter": [
        "lowercase",
        "decimal_digit",
        "arabic_normalization",
        "persian_normalization",
        "remove_suffix_m",
        "remove_suffix_am",
    ],
}
persian_search_analyzer = deepcopy(persian_index_analyzer)
persian_search_analyzer["filter"].append("synonyms")
# stop should happen after synonym other wive elastic crash
# e.g in تب و لرز, مالاریا
# see https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-graph-tokenfilter.html#_stop_token_filter_before_synonym_token_filter_2
# stop word also should be before stemmer other wise some additional words would be deleted
# e.g : بینی -> بین 
persian_index_analyzer["filter"].extent(["persian_stop", "persian_stemmer"])
persian_search_analyzer["filter"].extent(["persian_stop", "persian_stemmer"])

settings = {
    "analysis": {
        "char_filter": {
            "zero_width_spaces": {
                "type": "mapping",
                "mappings": ["\\u200C=>\\u0020", "-=>\\u0020", "_=>\\u0020"],
            }
        },
        "filter": {
            "persian_stop": {"type": "stop", "stopwords": "_persian_"},
            "persian_stemmer": {"type": "stemmer", "language": "persian"},
            "remove_suffix_m": {
                "type": "pattern_replace",
                "pattern": "م$",
                "replacement": "",
            },
            "remove_suffix_am": { # چشام؛ 
                "type": "pattern_replace",
                "pattern": "ام$",
                "replacement": "",
            },
            "synonyms": {
                "type": "synonym_graph",
                "synonyms_set": "synonyms-set",
                "updateable": True,
            },
        },
        "analyzer": {
            "default": persian_index_analyzer,
            "default_search": persian_search_analyzer,
        },
    }
}


def create_index(mappings, settings, index_name="doctors", reindex=True):
    if es.indices.exists(index="doctors").raw:
        if not reindex:
            return
        es.indices.delete(index="doctors")
    if 0 < es.synonyms.get_synonyms_sets()["count"]:
        es.synonyms.delete_synonym(id="synonyms-set")
    with open("synonyms.txt") as f:
        synonyms = [s for s in f.readlines()]
    es.synonyms.put_synonym(
        id="synonyms-set",
        synonyms_set=[{"id": f"{i}", "synonyms": s} for i, s in enumerate(synonyms)],
    )
    es.indices.create(
        index=index_name,
        mappings=mappings,
        settings=settings,
    )


def index(
    data, mappings=mappings, settings=settings, index_name="doctors", reindex=True
):
    create_index(mappings, settings, index_name, reindex)
    for i, row in data.iterrows():
        doc = {
            "expertise": row["display_expertise"],
            "gender": row["gender"],
            "experience": row["experience"],
            "title": row["title"],
            "star": row["star"],
            "rates_count": row["rates_count"],
            "number_of_visits": row["number_of_visits"],
            "view": row["view"],
            "insurances": row["insurances"],
            "doctor_encounter": row["doctor_encounter"],
            "explanation_of_issue": row["explanation_of_issue"],
            "quality_of_treatment": row["quality_of_treatment"],
            "comments_count": row["comments_count"],
            # large amount if it does not exist to get a small score look at blew comments
            "waiting_time": row["waiting_time"] if row["waiting_time"] else 4,
            "medical_code": row["medical_code"],
            "clinic": row["clinic"],
            "url": row["url"],
            "image": row["image"],
            # look at https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html#_what_if_a_field_is_missing
            # https://github.com/elastic/elasticsearch/issues/7788 https://github.com/elastic/elasticsearch/issues/18892
            "presence_freeturn": row["presence_freeturn"]
            if row["presence_freeturn"]
            else 0,
            "about": row["about"],
        }
        es.index(index="doctors", id=i, document=doc)


def get_data(path):
    data = pd.read_csv(path + "base_dataset.csv")
    about = pd.read_csv(path + "about_dataset.csv")
    data["clinic"] = data["clinic"].apply(safe_literal_eval)
    # data["insurances"] = data["insurances"].apply(safe_literal_eval) TODO
    data = data.replace(np.nan, None)
    about = about.replace(np.nan, None)
    data["about"] = about["about"]
    return data


if __name__ == "__main__":
    data = get_data("../data/processed/")
    index(data)
