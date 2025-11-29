# Doctor search

This project aims to search and suggest doctors base on the user input (voice or text)

For example, you can search for `The best internal medicine doctor with short waiting time` and get results.

### data source
data is collected from paziresh24

there about 79k doctors data

### Technologies
- google api for voice to text conversion
- streamlit for ui
- bert for token classification as base model
- hugging face for loading base model and fine tuning
- onnx cuad and tensorrt for model serving
- docker and docker compose
-  elastic search for searching through doctors
## Executing program
```
docker compose up
```
open following url

http://localhost:8501/

## Links
### google drive for documentation
https://drive.google.com/drive/folders/1WjvBrvEzrj9t1vvRpjwyIggdh0K6DQ3D
### github
https://github.com/smhd001/hammasir

## project structure
```
.
├── app
│   ├── config.py
│   ├── Dockerfile
│   ├── elastic_query.py
│   ├── query_config.py
│   ├── requirement.txt
│   ├── slot_filing.py
│   ├── test.ipynb
│   └── ui.py
├── doctors_data
│   ├── crawl
│   ├── data
│   └── elastic
├── slot_filling
│   ├── data_gathering
│   ├── read_data.py
│   └── training
├── docker-compose.yml
```
This is the overall structure of project for more details visit each part's README
### app
this part is for serving model and ui 

also queries are created and send to elastic
### doctors data
this part is for crawling data and processing and indexing in elastic search

### slot_filling
this part is for training and data collection for slot filling model

## Authors

Contributors names and contact info

- Sina Ramezani @sinar77
- Mohmmad Hashemy @smhd001 @hammasirpc

## acknowledgment
https://www.paziresh24.com/

for their api

Mohammad Amin @mohamin1995 and taha

and every body who helps us for data gathering
