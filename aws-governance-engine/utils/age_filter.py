from datetime import datetime, timezone
from config import AGE_THRESHOLD_DAYS

def is_old_enough(resource_time):
    if AGE_THRESHOLD_DAYS == 0:
        return True
    age = (datetime.now(timezone.utc) - resource_time).days
    return age >= AGE_THRESHOLD_DAYS