import os
import sys

module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)

from elasticsearch import Elasticsearch  # noqa: E402, F401
from query_config import query_config  # noqa: E402

# # Connect to Elasticsearch
# es = Elasticsearch(
#     "https://localhost:9200",
#     basic_auth=("elastic", "hammasir"),
#     verify_certs=False,
#     ssl_show_warn=False,
# )
# print(es.info())


def search(search_params) -> list[str]:
    result = dummy_query(search_params)
    # final_query = build_query(search_params, query_config)
    # result = es.search(index="doctors", body={"query": final_query})
    return format_result(result)


def build_query(search_params, config=query_config):
    query = {"bool": {"must": [], "should": [], "filter": []}}

    for field in ["problem", "expertise"]:
        if field in search_params:
            query["bool"]["should"].extend(
                [{"match": {"expertise": e}} for e in search_params[field]]
            )

    if "city" in search_params:
        query["bool"]["filter"].append(
            {"term": {"clinic.city": search_params["city"][0]}}
        )

    if "gender" in search_params:
        query["bool"]["filter"].append({"term": {"gender": search_params["gender"][0]}})

    final_query = {
        "function_score": {
            "query": query,
            "functions": [
                {
                    "field_value_factor": {
                        "field": "star",
                        "factor": config["factors"]["star"],
                        "modifier": "none",
                        "missing": 0,
                    }
                },
                {
                    "field_value_factor": {
                        "field": "rating",
                        "factor": config["factors"]["rating"],
                        "modifier": "none",
                        "missing": 0,
                    }
                },
            ],
            "boost_mode": "sum",
            "score_mode": "sum",
        }
    }

    return final_query


def dummy_query(text):
    # fmt: off
    return {"took": 21, "timed_out": False, "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0}, "hits": { "total": {"value": 2, "relation": "eq"}, "max_score": 13.364021, "hits": [ { "_index": "doctors", "_id": "10820", "_score": 13.364021, "_source": { "expertise": "ماما", "gender": "F", "experience": None, "title": "محبوبه رستگارراد", "star": 5.0, "rates_count": 1.0, "number_of_visits": 1035.0, "view": "1K", "insurances": "[]", "doctor_encounter": 5.0, "explanation_of_issue": 5.0, "quality_of_treatment": 5.0, "comments_count": 1.0, "url": "/%D8%AF%DA%A9%D8%AA%D8%B1-%D9%85%D8%AD%D8%A8%D9%88%D8%A8%D9%87-%D8%B1%D8%B3%D8%AA%DA%AF%D8%A7%D8%B1-%D8%B1%D8%A7%D8%AF", "lat": "36.30973606873734", "lon": "59.5287704437678", "waiting_time": 0.0, "image": "/getImage/p24/search-women/5a46e1d7ee1eaf8fa43120ecce0c16e2.png?size=150", "clinic": [ { "city": "مشهد", "number": None, "address": "مشهد، بلوار حر، بین حر 7  و 9", "province_name": "خراسان رضوی", } ], }, }, { "_index": "doctors", "_id": "10758", "_score": 9.523348, "_source": { "expertise": "زنان _ مامایی _ ماما همراه _ ناباروری", "gender": "F", "experience": None, "title": "صابری مفرد", "star": 5.0, "rates_count": 18.0, "number_of_visits": 1457.0, "view": "1K", "insurances": "[]", "doctor_encounter": 5.0, "explanation_of_issue": None, "quality_of_treatment": 5.0, "comments_count": 9.0, "waiting_time": 0.0, "image": "/getImage/p24/search-women/c3998d645d48d0580494589c72028da2.jpg?size=150", "url": "/%D8%AF%DA%A9%D8%AA%D8%B1-%D9%85%D8%B1%DB%8C%D9%85-%D8%B5%D8%A7%D8%A8%D8%B1%DB%8C-%D9%85%D9%81%D8%B1%D8%AF", "lat": "36.30973606873734", "lon": "59.5287704437678", "clinic": [ { "city": "مشهد", "number": "09150461628", "address": "مشهد، احمدآباد حدفاصل محتشمی و عارف (پشت ایستگاه مترو قائم) ساختمان پزشکان فرید طبقه دوم واحد 202", "province_name": "خراسان رضوی", }, { "city": "تهران", "number": "02125015555", "address": "مرکز ویزیت آنلاین پذیرش24", "province_name": "تهران", }, ], }, }, ], }, }
    # fmt: on


def format_result(result) -> list[str]:
    formatted_result = []
    for hits in result["hits"]["hits"]:
        name = hits["_source"]["title"]
        expertise = hits["_source"]["expertise"]
        url = hits["_source"]["url"]
        titel = name + "\n\n" + expertise
        description = hits["_source"]
        formatted_result.append((titel, url, description))
    return formatted_result
