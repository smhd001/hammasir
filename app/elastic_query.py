import json
from elasticsearch import Elasticsearch


# Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "hammasir"),
    verify_certs=False,
    ssl_show_warn=False,
)
print(es.info())


def search(slots) -> str:
    result = query(slots)
    return format_result(result)


def query(search_params, index_name="doctors"):
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
    print(query)

    return es.search(index=index_name, body={"query": query})


def format_result(result) -> str:
    formated_result = []
    for hits in result["hits"]["hits"]:
        name = hits["_source"]["title"]
        expertise = hits["_source"]["expertise"]
        titel = name + "\n\n" + expertise
        description = json.dumps(hits["_source"], indent=2, ensure_ascii=False)
        formated_result.append((titel, description))
    return formated_result
