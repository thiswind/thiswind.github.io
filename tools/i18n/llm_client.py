import os

from openai import OpenAI

from config import LLM_BASE_URL, LLM_MODEL


def get_client():
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise RuntimeError("LLM_API_KEY is required")
    return OpenAI(api_key=api_key, base_url=LLM_BASE_URL, timeout=90.0, max_retries=1)


def complete(messages, temperature=0.25):
    client = get_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()
