from .clients import openai_client
from typing import List, Dict

model = "gpt-4.1-mini"


def completion(messages: List[Dict[str, str]] = [], tools: List[Dict] = None):
    kwargs = {
        "model": model,
        "messages": messages
    }
    
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    
    response = openai_client.chat.completions.create(**kwargs)
    return response.choices[0].message
