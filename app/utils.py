from .prompts import qa_template,qa_template2
# File: utils.py
from langchain.prompts import PromptTemplate


# Wrap prompt template in a PromptTemplate object
def set_qa_prompt():
    prompt = PromptTemplate(template=qa_template,
                            input_variables=['context', 'question'])
    return prompt

def set_qa_prompt2():
    prompt = PromptTemplate(template=qa_template2,
                            input_variables=['test','submission'])
    return prompt


import re

def detect_percentage(text):
    # Define a regex pattern to match percentage values
    pattern = r'(\d+(?:\.\d+)?)%'  # Matches one or more digits followed by a '%' sign

    # Search for the pattern in the text
    match = re.search(pattern, text)

    # If a match is found, extract the percentage value
    if match:
        percentage = float(match.group(1))
        return percentage
    else:
        return None
