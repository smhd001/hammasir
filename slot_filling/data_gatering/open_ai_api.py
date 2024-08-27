import os
import sys
from os import path
from random import sample

import openai

module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)

from read_data import tag_names  # noqa: E402

NUM_SENTENCES_GENERATION_EXAMPLES = 5
NUM_LABELING_SENTENCES = 5

# address of prompt files
SENTENCE_GENERATION_FILE_PATH = path.join(
    path.dirname(__file__), "prompts", "sentence_generation.txt"
)
LABELING_FILE_PATH = path.join(path.dirname(__file__), "prompts", "labeling.txt")
LABELLING_EXAMPLES_FILE_PATH = path.join(
    path.dirname(__file__), "prompts", "labeling_examples.txt"
)


def sample_sentence_from_file(file_path, n) -> list[str]:
    with open(file_path, "r") as file:
        sentences = file.readlines()
    return sample(sentences, n)


def sample_sentence(n) -> str:
    return "\n".join(["123", "456", "789"])
    # return "\n".join(sample_sentence_from_file("sentences.txt", n))


def get_sentence_generation_prompt() -> str:
    prompt = open(SENTENCE_GENERATION_FILE_PATH, "r").read()
    return prompt.format(examples=sample_sentence(NUM_SENTENCES_GENERATION_EXAMPLES))


def get_labeling_prompt(sentences: str) -> str:
    prompt = open(LABELING_FILE_PATH, "r").read()
    examples = open(LABELLING_EXAMPLES_FILE_PATH, "r").read()
    return prompt.format(tags=tag_names + ["O"], examples=examples, sentences=sentences)
