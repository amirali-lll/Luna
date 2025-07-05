from datetime import datetime

def get_current_in_local_time() -> dict:
    """
    Get the current date and time in the local timezone.
    Returns the current time as a formatted string with timezone information.
    """
    return {"time": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")}