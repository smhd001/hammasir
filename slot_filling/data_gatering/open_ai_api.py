import enum
import os
import sys
from datetime import datetime
from random import sample

import openai

import config

module_path = os.path.abspath(os.path.join(".."))
if module_path not in sys.path:
    sys.path.append(module_path)

from read_data import all_tags_list  # noqa: E402
from preprocessing import gpt_sentence_generated_postprocessing  # noqa: E402


def sample_sentence_from_file(file_path: str, n) -> list[str]:
    sentences = ""
    with open(file_path + "/team.txt", "r") as file:
        sentences = file.readlines()
    with open(file_path + "/human.txt", "r") as file:
        sentences += file.readlines()
    return sample(sentences, n)


def sample_sentence(n) -> str:
    return "".join(sample_sentence_from_file(config.SENTENCE_EXAMPLE_DIR, n))


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


ChatMethod = enum.Enum("ChatMethod", ["api", "ui", "selenium"])


def chat_ui(prompt: str, generation_config) -> str:
    """copy to chat and paste response here"""
    print(prompt)
    result = ""
    while True:
        response = input()
        if response == "e":
            break
        result += response + "\n"
    return result


def chat_selenium(prompt: str, generation_config) -> str:
    pass


def chat_aip(prompt: str, generation_config) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        **generation_config,
    )
    return response.choices[0].message["content"]


def chat(
    prompt: str, generation_config, chat_method: ChatMethod = ChatMethod.ui
) -> str:
    match chat_method:
        case ChatMethod.api:
            return chat_aip(prompt, generation_config)
        case ChatMethod.ui:
            return chat_ui(prompt, generation_config)
        case ChatMethod.selenium:
            return chat_selenium(prompt, generation_config)
        case _:
            raise ValueError("Invalid ChatMethod")


def generate_sentence(n):
    generation_config = config.SENTENCE_GENERATION_CONFIG
    result = ""
    for _ in range(n // config.NUM_SENTENCES_OUTPUT):
        prompt = get_sentence_generation_prompt()
        response = chat(prompt, generation_config)
        result += response + "\n"
    result = gpt_sentence_generated_postprocessing(result)
    # save generated sentences
    with open(
        config.SENTENCE_GENERATED_DIR_PATH
        + "/gpt/"
        + f"{datetime.now().strftime('%Y%m%d%H%M%S')}.txt",
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
            response = chat(prompt, generation_config)
            if response[-1] != "\n":
                response += "\n"
            result += response
        with open(
            config.LABELING_DIR_PATH + "/gpt/" + f,
            "w",
        ) as file:
            file.write(result)


if __name__ == "__main__":
    generate_sentence(10)
    generate_labeling()
