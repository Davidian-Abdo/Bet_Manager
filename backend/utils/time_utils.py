from datetime import datetime, timedelta

def get_current_time():
    return datetime.utcnow()

def working_days_between(start_date: datetime, end_date: datetime) -> int:
    day_count = (end_date - start_date).days + 1
    return sum(1 for i in range(day_count)
               if (start_date + timedelta(days=i)).weekday() < 5)