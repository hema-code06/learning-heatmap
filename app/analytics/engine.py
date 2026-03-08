from datetime import datetime, timedelta
from statistics import mean, stdev
from collections import defaultdict



def calculate_daily_streak(entries):

    if not entries:
        return 0

    today = datetime.utcnow().date()

    day_topics = defaultdict(set)

    for e in entries:
        day_topics[e.date].add(e.topic)

    streak = 0
    current = today

    while True:

        topics_today = len(day_topics.get(current, []))

        if topics_today >= 3:
            streak += 1
            current -= timedelta(days=1)
        else:
            break

    return streak


