import json

import requests
from bs4 import BeautifulSoup

doctors_data = []
expertise_list = []
city_list = []


def get_json(city, expertise):
    for num in range(1, 26):
        url = f"https://apigw.paziresh24.com/v1/search/{city}/{expertise}/?page={num}"
        print(url)
        response = requests.get(url)
        data = response.json()
        search = data.get("search")
        result = search.get("result")
        if result:
            result["city"] = city
            doctors_data.extend(result)
        else:
            return


def get_expertise():
    url = "https://www.paziresh24.com/s/"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    ul_class_name = "list-none flex flex-col overflow-auto scrollBar"
    ul_element = soup.find("ul", class_=ul_class_name)

    expertise_list = []
    if ul_element:
        li_elements = ul_element.find_all("li")

        for li in li_elements:
            a_tag = li.find("a")
            if a_tag and a_tag.has_attr("href"):
                href_value = a_tag["href"]
                expertise_list.append(href_value[6:-1])
                # print(href_value[6:-1])
    else:
        print(f"No <ul> found with class '{ul_class_name}'")

    return expertise_list


def get_all_data(city_list, expertise_list):
    count = 0
    for city in city_list:
        for expertise in expertise_list:
            get_json(city, expertise)
            print(count)


expertise_list = get_expertise()
city_list = ["tehran", "mashhad"]
get_all_data(city_list, expertise_list)

with open("doctors.json", "w", encoding="utf-8") as file:
    json.dump(doctors_data, file, ensure_ascii=False, indent=4)
