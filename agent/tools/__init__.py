from .clock import get_current_time
from .utils import build_tools
from .remotes import remote_tools



built_in_tools = build_tools(
    [
        get_current_time
    ]
)

# Create a mapping of function names to actual functions
def get_tool_functions():
    return {
        "get_current_time": get_current_time
    }



def get_tools():
    """
    Returns a list of all tools, including built-in and remote tools.
    """
    return built_in_tools 