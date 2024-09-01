import re
ZWNJ = "\u200c"
def gpt_sentence_generated_postprocessing(text):
    text = text.replace(ZWNJ, " ")
    return re.sub(r"\d+\. ", "", text)
