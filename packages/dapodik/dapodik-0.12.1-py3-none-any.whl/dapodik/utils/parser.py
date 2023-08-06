from datetime import datetime, date
from typing import Union


def str_to_datetime(
    data: Union[str, datetime], format: str = "%Y-%m-%d %H:%M:%S"
) -> datetime:
    if isinstance(data, datetime):
        return data
    elif type(data) == str:
        if "." in data:
            return datetime.strptime(data, format + ".%f")
        return datetime.strptime(data, format)
    else:
        return datetime.now()


def str_to_date(data: Union[str, date], format: str = "%Y-%m-%d") -> date:
    if isinstance(data, date):
        return data
    elif type(data) == str:
        return datetime.strptime(data, format).date()
    else:
        return datetime.now().date()
