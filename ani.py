from dateutil import tz
from datetime import datetime, timezone
import pandas as pd

def timezone_adjust(dataset, column):
    changed_time = pd.to_datetime(dataset[column], unit='s')
    changed_time = [x.to_pydatetime() for x in changed_time]
    changed_time = [x.replace(tzinfo=timezone.utc) for x in changed_time]
    LA = tz.gettz('America/Los_Angeles')
    changed_time = [x.astimezone(LA) for x in changed_time]
    dataset[column] = changed_time

