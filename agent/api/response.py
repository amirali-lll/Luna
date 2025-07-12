from typing import AsyncGenerator, List, Dict, Union
from openai import AsyncOpenAI

async_openai_client = AsyncOpenAI()

async def streaming_response(
    input: Union[str, List[Dict[str, str]]] = "",
    tools: List[Dict] = None,
    model: str = "gpt-4o",
    **kwargs
) -> AsyncGenerator[Union[str, List[Dict]], None]:
    """
    Stream output from OpenAI's Responses API with support for tool calls.
    
    Yields:
        - str chunks (for normal text content)
        - List[Dict] tool_calls (when tool calls are complete)
    """
    # Prepare request payload
    request_kwargs = {
        "model": model,
        "input": input,
        "stream": True,
    }

    if tools:
        request_kwargs["tools"] = tools
        request_kwargs["tool_choice"] = "auto"

    # Add any extra kwargs like temperature, etc.
    request_kwargs.update(kwargs)

    # Initiate stream from OpenAI Responses API
    stream = await async_openai_client.responses.create(**request_kwargs)

    accumulated_tool_calls = {}

    async for event in stream:
        if event.type == "response.output_text.delta":
            delta = event.data.delta
            if delta.text:
                yield delta.text

        elif event.type == "response.tool_call":
            # Handle tool call streaming parts
            call = event.data
            index = call.index

            if index not in accumulated_tool_calls:
                accumulated_tool_calls[index] = {
                    "id": call.call_id,
                    "type": call.type or "function",
                    "function": {
                        "name": call.name or "",
                        "arguments": call.arguments or ""
                    }
                }
            else:
                if call.name:
                    accumulated_tool_calls[index]["function"]["name"] += call.name
                if call.arguments:
                    accumulated_tool_calls[index]["function"]["arguments"] += call.arguments

        elif event.type == "response.tool_calls.completed":
            if accumulated_tool_calls:
                tool_calls = list(accumulated_tool_calls.values())
                yield tool_calls
                accumulated_tool_calls.clear()

        elif event.type == "response.completed":
            break