from os import path

NUM_SENTENCES_GENERATION_EXAMPLES = 5
NUM_SENTENCES_OUTPUT = 10
NUM_LABELING_SENTENCES = 5
# address of prompt files
SENTENCE_GENERATION_PROMPT_PATH = path.join(
    path.dirname(__file__), "prompts", "sentence_generation.txt"
)
SENTENCE_EXAMPLE_DIR = path.join(
    path.dirname(__file__),
    "data",
    "sentences",
    "human",
)
SENTENCE_GENERATED_DIR_PATH = path.join(path.dirname(__file__), "data", "sentences")

LABELING_PROMPT_PATH = path.join(path.dirname(__file__), "prompts", "labeling.txt")
LABELLING_EXAMPLES_FILE_PATH = path.join(
    path.dirname(__file__), "prompts", "labeling_examples.txt"
)
LABELING_DIR_PATH = path.join(path.dirname(__file__), "data", "ladeled")

MERGED_FILE_PATH = path.join(path.dirname(__file__), "data", "merged.csv")
SENTENCE_GENERATION_CONFIG = {
    "max_tokens": 10000,
    "temperature": 0.7,  # higher temperature for more randomness
    "top_p": 0.9,
}

LABELING_GENERATION_CONFIG = {
    "max_tokens": 1000,
    "temperature": 0.3,  # lower temperature for more certainty
    "top_k": 1,  # model act deterministically
}
