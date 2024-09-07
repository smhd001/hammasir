import os
import sys

import evaluate
import numpy as np
from datasets import (
    ClassLabel,
    Dataset,
    DatasetDict,
    Features,
    NamedSplit,
    Sequence,
    Value,
)
from transformers import AutoModelForTokenClassification, AutoTokenizer

module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)
from read_data import read_data, tags_list  # noqa: E402


def get_model(model_id, freeze_base=False) -> tuple:
    if "roberta" in model_id:
        tokenizer = AutoTokenizer.from_pretrained(model_id, add_prefix_space=True)
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
    id2label = {i: label for i, label in enumerate(tags_list)}
    label2id = {v: k for k, v in id2label.items()}
    model = AutoModelForTokenClassification.from_pretrained(
        model_id,
        num_labels=len(id2label),
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )
    for param in model.parameters():
        param.data = param.data.contiguous()
    if freeze_base:
        for name, param in model.named_parameters():
            if "bert" in name:
                param.requires_grad = False
    return tokenizer, model


def tokenize_and_align_labels(examples, tokenizer):
    tokenized_inputs = tokenizer(
        examples["tokens"], truncation=True, is_split_into_words=True
    )

    labels = []
    for i, label in enumerate(examples["tags"]):
        word_ids = tokenized_inputs.word_ids(
            batch_index=i
        )  # Map tokens to their respective word.
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:  # Set the special tokens to -100.
            if word_idx is None:
                label_ids.append(-100)
            elif (
                word_idx != previous_word_idx
            ):  # Only label the first token of a given word.
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


def get_dataset(file_path, tokenizer, test_size=0.2) -> DatasetDict:
    data = read_data(file_path)
    sample = Dataset.from_list(
        data,
        features=Features(
            {
                "id": Value("int32"),
                "tokens": Sequence(Value("string")),
                "tags": Sequence(ClassLabel(names=tags_list)),
            }
        ),
        split=NamedSplit("train"),
    )
    sample = sample.train_test_split(test_size=test_size)
    tokenized_data = sample.map(
        tokenize_and_align_labels, batched=True, fn_kwargs={"tokenizer": tokenizer}
    )
    return tokenized_data


seqeval = evaluate.load("seqeval")


def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [
        [tags_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [tags_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = seqeval.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }
