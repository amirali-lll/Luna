from .clients import openai_client, async_openai_client
from typing import List, Dict, AsyncGenerator
import asyncio

model = "gpt-4.1-mini-2025-04-14"


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


async def streaming_completion(messages: List[Dict[str, str]] = [], tools: List[Dict] = None) -> AsyncGenerator[str, None]:
    """Stream completion response asynchronously."""
    kwargs = {
        "model": model,
        "messages": messages,
        "stream": True
    }
    
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    
    stream = await async_openai_client.chat.completions.create(**kwargs)
    
 
    
    async for chunk in stream:
        choice = chunk.choices[0]
        if choice.delta.content is not None:
            yield choice.delta.content
        elif choice.delta.tool_calls:
            yield choice.delta.tool_calls
