from datetime import date, datetime


def str_to_date(data: str) -> date:
    datas = data.split("-")
    return date(datas[0], datas[1], datas[2])


def str_to_datetime(data: str) -> datetime:
    dates, time = data.split(" ")
    d = str_to_date(dates)
    times = time.split(":")
    return datetime(d.year, d.month, d.day, times[0], times[1], times[2])
