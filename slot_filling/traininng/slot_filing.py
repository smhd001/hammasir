from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline

model = ORTModelForSequenceClassification.from_pretrained(
    "/home/ham/hammasir/hammasir/slot_filling/traininng/ner_model/checkpoint-4",
    export=True,
    provider="TensorrtExecutionProvider",
    from_transformers=True,
)


model_id = "HooshvareLab/bert-base-parsbert-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_id)
classifier = pipeline("ner", model=model, tokenizer=tokenizer)


def slot_fiiling(text) -> dict[str, str]:
    output = classifier(text)
    result = {}
    word = ""
    last_tag = None
    for en in output:
        boi, tag = en["entity"].split("-", 1)
        if boi == "B":
            if word:
                result.setdefault(last_tag, []).append(word.strip())
            word = en["word"] + " "
        elif boi == "I":
            word += en["word"] + " "
        else:
            raise ValueError("tags most start with B or I")
        last_tag = tag
    if word:
        result.setdefault(last_tag, []).append(word.strip())
    return result
