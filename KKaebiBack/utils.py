from datetime import date, timedelta
from Housework.models import Housework


# 사용자 완료 비율 및 레벨 계산
def calculate_user_statistics(user, start_date=None, end_date=None):
    if not start_date or not end_date:
        today = date.today()
        start_date = today
        end_date = today

    tasks = Housework.objects.filter(user=user, houseworkDate__range=[start_date, end_date])
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(houseworkDone=True).count()
    completion_rate = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

    return total_tasks, completed_tasks, completion_rate

# 오늘 완료율 계산
def calculate_today_completion_rate(user):
    today = date.today()
    _, _, today_completion_rate = calculate_user_statistics(user, start_date=today, end_date=today)
    return today_completion_rate

# 일주일 완료율 계산
def calculate_weekly_completion_rate(user):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # 월요일
    end_of_week = start_of_week + timedelta(days=6)  # 일요일
    _, _, weekly_completion_rate = calculate_user_statistics(user, start_date=start_of_week, end_date=end_of_week)
    return weekly_completion_rate


def calculate_level(completion_rate):
    if completion_rate == 100:
        return "Lv7. 빛"
    elif completion_rate >= 99:
        return "Lv6. 청소 탐험가"
    elif completion_rate >= 80:
        return "Lv5. 향기 탐험가"
    elif completion_rate >= 60:
        return "Lv4. 먼지 사냥꾼"
    elif completion_rate >= 40:
        return "Lv3. 티끌 수집가"
    elif completion_rate >= 20:
        return "Lv2. 먼지"
    else:
        return "Lv1. 미세먼지"

