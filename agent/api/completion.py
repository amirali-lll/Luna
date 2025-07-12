from .clients import *
from typing import List, Dict, AsyncGenerator, Union
from typing import List, Dict, AsyncGenerator


default_model = "gpt-4.1-mini-2025-04-14"


def completion(messages: List[Dict[str, str]] = [], tools: List[Dict] = None):
    kwargs = {
        "model": default_model,
        "messages": messages
    }
    
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    
    response = openai_client.chat.completions.create(**kwargs)
    return response.choices[0].message


async def streaming_completion(
    messages: List[Dict[str, str]] = [],
    tools: List[Dict] = None,
    model: str = default_model,
    client: Union[AsyncOpenAI, OpenAI] = async_openai_client
) -> AsyncGenerator[str, None]:
    """Stream completion response asynchronously."""
    kwargs = {
        "model": model,
        "messages": messages,
        "stream": True
    }
    
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    stream = await client.chat.completions.create(**kwargs)

    accumulated_tool_calls = {}
    
    async for chunk in stream:
        choice = chunk.choices[0]
        if choice.delta.content is not None:
            yield choice.delta.content
        elif choice.delta.tool_calls:
            # Accumulate tool calls by index
            for tool_call_delta in choice.delta.tool_calls:
                index = tool_call_delta.index
                
                # Initialize if first time seeing this index
                if index not in accumulated_tool_calls:
                    accumulated_tool_calls[index] = {
                        "id": tool_call_delta.id,
                        "type": tool_call_delta.type or "function",
                        "function": {
                            "name": tool_call_delta.function.name or "",
                            "arguments": tool_call_delta.function.arguments or ""
                        }
                    }
                else:
                    # Accumulate the pieces
                    if tool_call_delta.id:
                        accumulated_tool_calls[index]["id"] = tool_call_delta.id
                    if tool_call_delta.type:
                        accumulated_tool_calls[index]["type"] = tool_call_delta.type
                    if tool_call_delta.function.name:
                        accumulated_tool_calls[index]["function"]["name"] += tool_call_delta.function.name
                    if tool_call_delta.function.arguments:
                        accumulated_tool_calls[index]["function"]["arguments"] += tool_call_delta.function.arguments
        elif choice.finish_reason == "tool_calls":
            # Tool calls are complete, convert to proper format and yield
            if accumulated_tool_calls:
                tool_calls = list(accumulated_tool_calls.values())
                yield tool_calls
                accumulated_tool_calls.clear()