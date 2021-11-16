from datetime import datetime


def same_date(date_1: datetime, date_2: datetime) -> bool:
    """
    Checks if two dates are the same month, day, and year
    """
    return date_1.date() == date_2.date()

def same_time(date_1: datetime, date_2: datetime) -> bool:
    """
    Checks if two dates are the same hour, minute, second and microsecond
    """
    return date_1.time() == date_2.time()

def same_datetime(date_1: datetime, date_2: datetime) -> bool:
    """
    Checks if two dates are the same datetime
    """
    return date_1 == date_2