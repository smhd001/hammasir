import json
import time
import requests
from bs4 import BeautifulSoup

doctors_data = []
expertise_list = []
city_list = []

def get_json(city, expertise):
    for num in range(1, 26):
        url = f"https://apigw.paziresh24.com/v1/search/{city}/{expertise}/?page={num}"
        print(url)
        retries = 3
        counter = 0
        for i in range(retries):
            response = requests.get(url)
        
            # Check if the response status is 200 (OK)
            if response.status_code != 200:
                print(f"Failed to fetch data: {response.status_code}")
                time.sleep(2 * i)
                continue
        
            # Try to decode the response as JSON
            try:
                data = response.json()
                break
            except requests.exceptions.JSONDecodeError as e:
                counter += 1
                print(f"Failed to decode JSON: {e}")
                print(f"Response content: {response.text}")  # Optional: print the response content
                time.sleep(1)
            except requests.exceptions.ConnectionError:
                print("Connection error")
                counter += 1
                time.sleep(2 * i)
        
        if counter == retries:
            continue

        search = data.get("search", {})
        result = search.get("result", [])
        
        if result:
            # Add city information to each doctor in the result list
            for doctor in result:
                doctor["city"] = city
            doctors_data.extend(result)
        else:
            print("No data found")
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
            count += 1
            print(count)


expertise_list = get_expertise()
city_list = ["tehran", "mashhad", "karaj", "ardabil", "bushehr", "shahrekord", "tabriz", "shiraz", "rasht", "gorgan", 
             "hamedan", "bandar-abbas", "ilam", "isfahan", "kerman", "kermanshah", "ahvaz", "yasuj", "sanandaj",
             "khorramabad", "arak", "sari", "bojnurd", "qazvin", "qom", "semnan", "zahedan", "birjand", "orumieh",
             "yazd", "zanjan"]


get_all_data(city_list, expertise_list)

with open("../data/raw/new_doctors.json", "w", encoding="utf-8") as file:
    json.dump(doctors_data, file, ensure_ascii=False)