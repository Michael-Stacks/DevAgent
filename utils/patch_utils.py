
import os, re
from langchain_community.llms import Ollama

MODEL = "mistral"

def extract_unified_diff(text):
    m = re.search(r"(^|\n)(-{3} a/.*?\n\+{3} b/.*?)(?=\n(?:-{3} a/|\Z))", text, flags=re.S)
    return m.group(2).strip() if m else ""

def generate_patch(instruction, context):
    llm = Ollama(model=MODEL)
    prompt = f"""You are a precise software engineer. Write a unified diff patch (`--- a/...`, `+++ b/...`)
    that implements the following instruction:
    Instruction:
    {instruction}

    Context:
    {context}

    Rules:
    - Output only the patch, no extra text.
    - Keep it minimal."""
    result = llm(prompt)
    diff = extract_unified_diff(result)
    if not diff:
        raise ValueError("No unified diff found in model output.")
    return diff
