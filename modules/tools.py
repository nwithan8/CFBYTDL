from datetime import datetime


def convert_string_to_datetime(date: str, from_format: str = '%Y-%m-%d %H:%M:%S') -> datetime:
    return datetime.strptime(date, from_format)


def convert_datetime_to_string(date: datetime, to_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    return date.strftime(to_format)


def convert_string_date_to_another_format(date: str, from_format: str = '%Y-%m-%d %H:%M:%S',
                                          to_format: str = '%Y-%m-%d') -> str:
    return convert_datetime_to_string(date=convert_string_to_datetime(date=date, from_format=from_format), to_format=to_format)
