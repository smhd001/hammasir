import os

from optimum.onnxruntime import ORTModelForTokenClassification
from transformers import AutoTokenizer, pipeline

# set model path if we are runnig in docker or no
if "DOCKER_CONTAINER" in os.environ:
    model_path = "/model"
else:
    model_path = "/home/ham/mlartifacts/867072811883705549/b23eda71b69548899cd3666c499206c3/artifacts/checkpoint-255/artifacts/checkpoint-255"

model = ORTModelForTokenClassification.from_pretrained(
    model_path,
    export=True,
    provider="CUDAExecutionProvider",
)

model_id = "ViraIntelligentDataMining/AriaBERT"
tokenizer = AutoTokenizer.from_pretrained(model_id)
classifier = pipeline("ner", model=model, tokenizer=tokenizer, device="cuda")


def slot_filing(text) -> dict[str, str]:
    output = classifier(text)
    result = {}
    word = ""
    last_tag = None
    last_end = 0
    for en in output:
        boi, tag = en["entity"].split("-", 1)
        if boi == "B":
            if word:
                result.setdefault(last_tag, []).append(word.strip())
            word = text[en["start"]:en["end"]]
            if en["start"] != last_end:
                word += " "
        elif boi == "I":
            if en["start"] != last_end:
                word += " "
            word += text[en["start"]:en["end"]] + " "
        else:
            raise ValueError("tags most start with B or I")
        last_tag = tag
        last_end = en["end"]
    if word:
        result.setdefault(last_tag, []).append(word.strip())
    return result

print(slot_filing("سرم درد می کنه یکی می خوام تو مشهد"))