import inspect
from typing import get_origin, get_args

type_map = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object"
}

def build_tools(functions):
    tools = []
    for func in functions:
        sig = inspect.signature(func)
        props = {}
        required = []

        for name, param in sig.parameters.items():
            annotation = param.annotation

            # Default to str if no type hint
            if annotation == inspect.Parameter.empty:
                annotation = str

            origin = get_origin(annotation)
            args = get_args(annotation)

            if origin is list and args:
                # Example: list[str]
                item_type = type_map.get(args[0], "string")
                param_schema = {
                    "type": "array",
                    "items": {"type": item_type},
                    "description": f"Parameter: {name}"
                }
            elif annotation in type_map:
                param_schema = {
                    "type": type_map[annotation],
                    "description": f"Parameter: {name}"
                }
            else:
                raise ValueError(f"Unsupported type for parameter '{name}' in function '{func.__name__}': {annotation}")

            props[name] = param_schema

            if param.default == inspect.Parameter.empty:
                required.append(name)

        tools.append({
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__ or "",
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": required
                }
            }
        })

    return tools
