import datetime

JSON_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
"""datetime format string for generating JSON content
"""

def datetimeToJsonStr(dt):
    if dt is None:
        return None
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        # Naive timestamp, convention is this must be UTC
        return f"{dt.strftime(JSON_TIME_FORMAT)}Z"
    return dt.strftime(JSON_TIME_FORMAT)


def _jsonConverter(o):
    if isinstance(o, datetime.datetime):
        return datetimeToJsonStr(o)
    return o.__str__()


def generateDayMatrix(tzones, for_date):
    t0 = for_date.astimezone()
    row = ['Local', ]
    for hr in range(0,24):
        dt = datetime.timedelta(hours=hr)
        t1 = t0 + dt
        row.append(t1)
    res = [row, ]
    for z in tzones:
        t0 = for_date
        t0 = t0.replace(minute=0, second=0, microsecond=0)
        row = [z.zone, ]
        for hr in range(0, 24):
            td = datetime.timedelta(hours=hr)
            t1 = t0 + td
            t2 = t1.astimezone(z)
            row.append(t2)
        res.append(row)
    return res
