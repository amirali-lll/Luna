from .clock import get_current_in_local_time
from .utils import build_tools

built_in_tools = build_tools(
    [
        get_current_in_local_time
    ]
)