import json
from elasticsearch import Elasticsearch


# Connect to Elasticsearch
# es = Elasticsearch(
#     "https://localhost:9200",
#     basic_auth=("elastic", "hammasir"),
#     verify_certs=False,
#     ssl_show_warn=False,
# )
# print(es.info())


def search(slots) -> str:
    # resualt = query(slots)
    result = {'took': 21, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 2, 'relation': 'eq'}, 'max_score': 13.364021, 'hits': [{'_index': 'doctors', '_id': '10820', '_score': 13.364021, '_source': {'expertise': 'ماما', 'gender': 'F', 'experience': None, 'title': 'محبوبه رستگارراد', 'star': 5.0, 'rates_count': 1.0, 'number_of_visits': 1035.0, 'view': '1K', 'insurances': '[]', 'doctor_encounter': 5.0, 'explanation_of_issue': 5.0, 'quality_of_treatment': 5.0, 'comments_count': 1.0, 'waiting_time': 0.0, 'clinic': [{'city': 'مشهد', 'number': None, 'address': 'مشهد، بلوار حر، بین حر 7  و 9', 'province_name': 'خراسان رضوی'}]}}, {'_index': 'doctors', '_id': '10758', '_score': 9.523348, '_source': {'expertise': 'زنان _ مامایی _ ماما همراه _ ناباروری', 'gender': 'F', 'experience': None, 'title': 'صابری مفرد', 'star': 5.0, 'rates_count': 18.0, 'number_of_visits': 1457.0, 'view': '1K', 'insurances': '[]', 'doctor_encounter': 5.0, 'explanation_of_issue': None, 'quality_of_treatment': 5.0, 'comments_count': 9.0, 'waiting_time': 0.0, 'clinic': [{'city': 'مشهد', 'number': '09150461628', 'address': 'مشهد، احمدآباد حدفاصل محتشمی و عارف (پشت ایستگاه مترو قائم) ساختمان پزشکان فرید طبقه دوم واحد 202', 'province_name': 'خراسان رضوی'}, {'city': 'تهران', 'number': '02125015555', 'address': 'مرکز ویزیت آنلاین پذیرش24', 'province_name': 'تهران'}]}}]}}
    return format_result(result)

def query(text):
    pass

def format_result(result) -> str:
    formated_result = []
    for hits in result["hits"]["hits"]:
        name = hits["_source"]["title"]
        expertise = hits["_source"]["expertise"]
        titel = name + "\n\n" + expertise
        description = json.dumps(hits["_source"], indent=2, ensure_ascii=False)
        formated_result.append((titel, description))
    return formated_result
