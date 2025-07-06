from datetime import datetime
import pytz

def get_current_time(timezone: str = "local") -> dict:
    """
    Get the current date and time in the specified timezone.
    If timezone is 'local', returns local time. Otherwise, uses the given timezone string (e.g., 'America/Los_Angeles').
    Returns the current time as a formatted string with timezone information.
    """
    if timezone == "local":
        now = datetime.now().astimezone()
    else:
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
        except Exception:
            return {"error": f"Invalid timezone: {timezone}"}
    return {"time": now.strftime("%Y-%m-%d %H:%M:%S %Z"), "timezone": str(now.tzinfo) if now.tzinfo else "UTC"}