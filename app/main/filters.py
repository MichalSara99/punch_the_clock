from . import main
from datetime import timedelta

@main.app_template_filter()
def formatTimedelta(delta):
    """Formats a timedelta duration to %H:%M:%S format"""
    if delta < timedelta(0):
        return '-' + formatTimedelta(-delta)
    else:
        seconds = int(delta.total_seconds())

        secs_in_a_day = 86400
        secs_in_a_hour = 3600
        secs_in_a_min = 60

        days, seconds = divmod(seconds, secs_in_a_day)
        hours, seconds = divmod(seconds, secs_in_a_hour)
        minutes, seconds = divmod(seconds, secs_in_a_min)

    time_fmt = f"{hours:02d}:{minutes:02d}"
    return time_fmt

@main.app_template_filter()
def formatTotalTimedelta(delta):
    """Formats a timedelta duration to %H:%M:%S format"""
    if delta < timedelta(0):
        return '-' + formatTimedelta(-delta)
    else:
        seconds = int(delta.total_seconds())

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

    time_fmt = f"{hours:02d}:{minutes:02d}"
    return time_fmt