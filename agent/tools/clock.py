from datetime import datetime

def get_current_in_local_time() -> dict:
    """
    Return the current time as a string.
    """
    return {"time": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")}