import os
import sys
from copy import deepcopy

module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)

from elasticsearch import Elasticsearch  # noqa: E402, F401
from query_config import query_config  # noqa: E402

# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "hammasir"),
    verify_certs=False,
    ssl_show_warn=False,
)
print(es.info())


def search(search_params) -> list[str]:
    # result = dummy_query(search_params)
    config = configure_query(search_params, query_config)
    final_query = build_query(search_params, config)
    result = es.search(index="doctors", body={"query": final_query})
    return format_result(result, search_params)


def configure_query(search_params, default_config):
    config = deepcopy(default_config)
    function_scores = {}
    for f_score, v in config["function_score"].items():
        if f_score in search_params:
            function_scores[f_score] = v
    function_scores["popularity"] = config["function_score"]["popularity"]
    config["function_score"] = function_scores
    # map gender
    if "gender" in search_params:
        for gender, g_terms in config["gender_map"].items():
            for g_term in g_terms:
                if g_term in search_params["gender"][0]:
                    search_params["gender"][0] = gender
    return config


def build_query(search_params, config=query_config):
    query = {"bool": {"must": [], "must_not": [], "should": [], "filter": []}}

    # between problem and expertise at least one should match
    problem_expertise_filter = []

    for search_p in ["problem", "expertise"]:
        if search_p in search_params:
            query["bool"]["should"].extend(
                [
                    bound_query(
                        query={
                            "match": {
                                "expertise": {
                                    "query": e,
                                    "fuzziness": 1,
                                    "boost": config["boosts"][search_p],
                                }
                            }
                        }
                    )
                    for e in search_params[search_p]
                ]
            )
            problem_expertise_filter.extend(
                [
                    {"match": {"expertise": {"query": e, "fuzziness": 1}}}
                    for e in search_params[search_p]
                ]
            )

    for term, search_in in [
        ("problem", "symptomes"),
        ("problem", "about"),
        ("expertise", "symptomes"),
        ("expertise", "about"),
    ]:
        if term in search_params:
            query["bool"]["should"].extend(
                [
                    bound_query(
                        query={
                            "match": {
                                search_in: {
                                    "query": e,
                                    "fuzziness": 1,
                                    "boost": config["boosts"][(term, search_in)],
                                }
                            }
                        }
                    )
                    for e in search_params[term]
                ]
            )
            print(search_in)
            problem_expertise_filter.extend(
                [
                    {"match": {search_in: {"query": e, "fuzziness": 1}}}
                    for e in search_params[term]
                ]
            )

    query["bool"]["filter"].append(({"bool": {"should": problem_expertise_filter}}))

    if "neighborhood" in search_params:
        query["bool"]["filter"].extend(
            [{"match": {"clinic.address": e}} for e in search_params["neighborhood"]]
        )

    if "city" in search_params:
        query["bool"]["filter"].append(
            {"term": {"clinic.city": search_params["city"][0]}}
        )

    if "insurance" in search_params:
        query["bool"]["filter"].extend(
            [{"match": {"insurances": e}} for e in search_params["insurance"]]
        )

    if "gender" in search_params:
        query["bool"]["filter"].append({"term": {"gender": search_params["gender"][0]}})

    if "first-available-appointment" in search_params:
        query["bool"]["must_not"].append({"term": {"presence_freeturn": 0}})

    query["bool"]["should"].extend(
        [bound_query(function=f) for f in list(config["function_score"].values())]
    )
    return query


def bound_query(*, query=None, function=None, maximum=5):
    # exactly one of these should not be None
    assert (query is not None) != (function is not None)
    if query:
        return {
            "function_score": {
                "query": query,
                "functions": [
                    {"script_score": {"script": {"source": "Math.min(5, _score)"}}}
                ],
                "boost_mode": "replace",
            }
        }

    return {
        "function_score": {
            "functions": [function, {"weight": maximum}],
            "score_mode": "min",
        }
    }


def build_query_v1(search_params, config=query_config):
    query = {"bool": {"must": [], "must_not": [], "should": [], "filter": []}}

    problem_expertise_query = {"bool": {"should": []}}
    for field in ["problem", "expertise"]:
        if field in search_params:
            problem_expertise_query["bool"]["should"].extend(
                [
                    {"match": {"expertise": {"query": e, "fuzziness": 1}}}
                    for e in search_params[field]
                ]
            )
    # (problem or experties) mus match
    query["bool"]["must"].append(problem_expertise_query)

    if "neighborhood" in search_params:
        query["bool"]["filter"].extend(
            [{"match": {"clinic.address": e}} for e in search_params["neighborhood"]]
        )

    if "city" in search_params:
        query["bool"]["filter"].append(
            {"term": {"clinic.city": search_params["city"][0]}}
        )

    if "insurance" in search_params:
        query["bool"]["filter"].extend(
            [{"match": {"insurances": e}} for e in search_params["insurance"]]
        )

    if "gender" in search_params:
        query["bool"]["filter"].append({"term": {"gender": search_params["gender"][0]}})

    if "first-available-appointment" in search_params:
        query["bool"]["must_not"].append({"term": {"presence_freeturn": 0}})

    query["bool"]["should"].extend(
        [
            {
                "function_score": {
                    "functions": [f, {"weight": 5}],
                    "score_mode": "min",
                }
            }
            for f in list(config["function_score"].values())
        ]
    )
    return query


def unrestricted_query(search_params, config=query_config):
    query = {"bool": {"must": [], "should": [], "filter": []}}

    for field in ["problem", "expertise"]:
        if field in search_params:
            query["bool"]["should"].extend(
                [
                    {"match": {"expertise": {"query": e, "fuzziness": 1}}}
                    for e in search_params[field]
                ]
            )

    if "neighborhood" in search_params:
        query["bool"]["filter"].extend(
            [{"match": {"clinic.address": e}} for e in search_params["neighborhood"]]
        )

    if "city" in search_params:
        query["bool"]["filter"].append(
            {"term": {"clinic.city": search_params["city"][0]}}
        )

    if "insurance" in search_params:
        query["bool"]["should"].extend(
            [{"match": {"insurance": e}} for e in search_params["insurance"]]
        )

    if "gender" in search_params:
        query["bool"]["filter"].append({"term": {"gender": search_params["gender"][0]}})

    final_query = {
        "function_score": {
            "query": query,
            "functions": list(config["function_score"].values()),
            "boost_mode": "sum",
            "score_mode": "sum",
        }
    }

    return final_query


def build_minimal_query(search_params, config=query_config):
    query = {"bool": {"must": [], "should": [], "filter": []}}

    for field in ["problem", "expertise"]:
        if field in search_params:
            query["bool"]["should"].extend(
                [
                    {"match": {"expertise": {"query": e, "fuzziness": 2}}}
                    for e in search_params[field]
                ]
            )

    if "city" in search_params:
        query["bool"]["filter"].append(
            {"term": {"clinic.city": search_params["city"][0]}}
        )

    if "gender" in search_params:
        query["bool"]["filter"].append({"term": {"gender": search_params["gender"][0]}})

    if "user-score" in search_params:
        functions = [{"star": config["function_score"]["star"]}]
    else:
        functions = []

    final_query = {
        "function_score": {
            "query": query,
            "functions": functions,
            "boost_mode": "sum",
            "score_mode": "sum",
        }
    }

    return final_query


def dummy_query(text):
    # fmt: off
    return {"took": 21, "timed_out": False, "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0}, "hits": { "total": {"value": 2, "relation": "eq"}, "max_score": 13.364021, "hits": [ { "_index": "doctors", "_id": "10820", "_score": 13.364021, "_source": { "expertise": "ماما", "gender": "F", "experience": None, "title": "محبوبه رستگارراد", "star": 5.0, "rates_count": 1.0, "number_of_visits": 1035.0, "view": "1K", "insurances": "[]", "doctor_encounter": 5.0, "explanation_of_issue": 5.0, "quality_of_treatment": 5.0, "comments_count": 1.0, "url": "/%D8%AF%DA%A9%D8%AA%D8%B1-%D9%85%D8%AD%D8%A8%D9%88%D8%A8%D9%87-%D8%B1%D8%B3%D8%AA%DA%AF%D8%A7%D8%B1-%D8%B1%D8%A7%D8%AF", "lat": "36.30973606873734", "lon": "59.5287704437678", "waiting_time": 0.0, "image": "/getImage/p24/search-women/5a46e1d7ee1eaf8fa43120ecce0c16e2.png?size=150", "clinic": [ { "city": "مشهد", "number": None, "address": "مشهد، بلوار حر، بین حر 7  و 9", "province_name": "خراسان رضوی", } ], }, }, { "_index": "doctors", "_id": "10758", "_score": 9.523348, "_source": { "expertise": "زنان _ مامایی _ ماما همراه _ ناباروری", "gender": "F", "experience": None, "title": "صابری مفرد", "star": 5.0, "rates_count": 18.0, "number_of_visits": 1457.0, "view": "1K", "insurances": "[]", "doctor_encounter": 5.0, "explanation_of_issue": None, "quality_of_treatment": 5.0, "comments_count": 9.0, "waiting_time": 0.0, "image": "/getImage/p24/search-women/c3998d645d48d0580494589c72028da2.jpg?size=150", "url": "/%D8%AF%DA%A9%D8%AA%D8%B1-%D9%85%D8%B1%DB%8C%D9%85-%D8%B5%D8%A7%D8%A8%D8%B1%DB%8C-%D9%85%D9%81%D8%B1%D8%AF", "lat": "36.30973606873734", "lon": "59.5287704437678", "clinic": [ { "city": "مشهد", "number": "09150461628", "address": "مشهد، احمدآباد حدفاصل محتشمی و عارف (پشت ایستگاه مترو قائم) ساختمان پزشکان فرید طبقه دوم واحد 202", "province_name": "خراسان رضوی", }, { "city": "تهران", "number": "02125015555", "address": "مرکز ویزیت آنلاین پذیرش24", "province_name": "تهران", }, ], }, }, ], }, }
    # fmt: on


def get_lat_long(result, city):
    for c in result["_source"]["clinic"]:
        if not city or c["city"] == city[0]:
            if c["lat"] and c["long"]:
                return c["lat"], c["long"]
    return None


def format_result(result, search_params) -> list[str]:
    formatted_result = []
    for hits in result["hits"]["hits"]:
        name = hits["_source"]["title"]
        expertise = hits["_source"]["expertise"]
        title = name + "\n\n" + expertise
        description = hits["_source"]
        lat_long = get_lat_long(hits, search_params.get("city", None))
        formatted_result.append((title, lat_long, description))
    return formatted_result
