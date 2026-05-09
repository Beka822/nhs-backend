from datetime import datetime,timedelta
def get_period_range(period:str):
    now=datetime.utcnow()
    if period=="today":
        start=now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    elif period=="week":
        start=now-timedelta(days=7)
    elif period=="month":
        start=now.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    elif period=="year":
        start=now.replace(
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    else:
        start=now.replace(day=1)
    return start.now