from .clock import get_current_in_local_time
from .utils import build_tools

built_in_tools = build_tools(
    [
        get_current_in_local_time
    ]
)

# Create a mapping of function names to actual functions
def get_tool_functions():
    return {
        "get_current_in_local_time": get_current_in_local_time
    }