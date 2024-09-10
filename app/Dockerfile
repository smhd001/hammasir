FROM nvcr.io/nvidia/tensorrt:24.08-py3

RUN apt-get update &&\
    apt-get install -y sudo git bash

WORKDIR app

COPY requirment.txt .

RUN pip install -r requirment.txt

COPY . .

ENTRYPOINT streamlit run ui.py