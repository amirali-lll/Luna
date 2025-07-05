from .clients import openai_client
from typing import List, Dict

model = "gpt-4.1-mini"


def completion(messages: List[Dict[str, str]] = []):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content
