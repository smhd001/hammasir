import os
import sys
from datetime import datetime
from random import sample

import config
import openai

module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)

from read_data import all_tags_list  # noqa: E402


def sample_sentence_from_file(file_path: str, n) -> list[str]:
    with open(file_path, "r") as file:
        sentences = file.readlines()
    return sample(sentences, n)


def sample_sentence(n) -> str:
    return "".join(sample_sentence_from_file(config.SENTENCE_EXAMPLE_FILE_PATH, n))


def get_sentence_generation_prompt() -> str:
    prompt = open(config.SENTENCE_GENERATION_PROMPT_PATH, "r").read()
    return prompt.format(
        examples=sample_sentence(config.NUM_SENTENCES_GENERATION_EXAMPLES),
        num_sentences=config.NUM_SENTENCES_OUTPUT,
    )


def get_labeling_prompt(sentences: str) -> str:
    prompt = open(config.LABELING_PROMPT_PATH, "r").read()
    examples = open(config.LABELLING_EXAMPLES_FILE_PATH, "r").read()
    return prompt.format(tags=all_tags_list, examples=examples, sentences=sentences)


def chat(prompt: str, generation_config):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        **generation_config,
    )
    return response.choices[0].message["content"]


def generate_sentence(n):
    generation_config = config.SENTENCE_GENERATION_CONFIG
    result = ""
    for _ in range(n // config.NUM_SENTENCES_OUTPUT):
        prompt = get_sentence_generation_prompt()
        response = chat(prompt, generation_config)
        result += response + "\n"
    # save generated sentences
    used_example_path = config.SENTENCE_EXAMPLE_FILE_PATH.split("/")[-1]
    with open(
        config.SENTENCE_GENERATED_DIR_PATH
        + "/gpt/"
        + f"{used_example_path}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt",
        "w",
    ) as file:
        file.write(result)


def generate_labeling(files: list[str] | None = None):
    if files is None:
        files = os.listdir(config.SENTENCE_GENERATED_DIR_PATH + "/gpt")
        annotated_files = os.listdir(config.LABELING_DIR_PATH + "/gpt")
        files = list(set(files) - set(annotated_files))
    for f in files:
        sentences = []
        with open(config.SENTENCE_GENERATED_DIR_PATH + "/gpt/" + f, "r") as file:
            sentences += file.readlines()
        # filter out empty lines
        sentences = [s.strip() for s in sentences if s.strip()]
        result = ""
        for i in range(len(sentences) // config.NUM_LABELING_SENTENCES):
            prompt = get_labeling_prompt(
                "\n".join(
                    sentences[
                        i * config.NUM_LABELING_SENTENCES : (i + 1)
                        * config.NUM_LABELING_SENTENCES
                    ]
                )
            )
            generation_config = config.LABELING_GENERATION_CONFIG
            result += chat(prompt, generation_config) + "\n"
        with open(
            config.LABELING_DIR_PATH + "/gpt/" + f,
            "w",
        ) as file:
            file.write(result)
