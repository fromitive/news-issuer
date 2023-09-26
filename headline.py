import datetime


def getHeadline():
    dom = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    now = datetime.date.today().isoformat()
    day_of_month = dom[datetime.date.today().weekday()]
    headline = now + " " + day_of_month + " 보안 주요뉴스"

    return headline, now
