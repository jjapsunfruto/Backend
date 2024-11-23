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
