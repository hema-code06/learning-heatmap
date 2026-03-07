from datetime import datetime, timedelta
from statistics import mean, stdev
from collections import defaultdict


# ------------------------------
# STREAK CALCULATIONS
# ------------------------------

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


def calculate_longest_streak(entries):
    if not entries:
        return 0

    dates = sorted({e.date() for e in entries})

    longest = 0
    current = 1

    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            current += 1
        else:
            longest = max(longest, current)
            current = 1

    return max(longest, current)


# ------------------------------
# LEARNING VELOCITY
# ------------------------------

def learning_velocity(entries):

    if not entries:
        return 0

    day_map = defaultdict(float)

    for e in entries:
        day_map[e.date] += e.hours

    daily_hours = list(day_map.values())

    return round(mean(daily_hours), 2)

# ------------------------------
# CONSISTENCY SCORE
# ------------------------------


def consistency_score(entries):
    if len(entries) < 2:
        return 50

    hours = [e.hours for e in entries]

    variability = stdev(hours)

    score = max(0, 100 - (variability * 20))

    return round(score, 2)


# ------------------------------
# TOPIC BREAKDOWN
# ------------------------------

def topic_breakdown(entries):
    topic_map = defaultdict(float)

    for e in entries:
        topic_map[e.topic] += e.hours

    total = sum(topic_map.values())

    return sorted(
    [
        {
            "topic": k,
            "hours": v,
            "percentage": round((v / total) * 100, 2) if total else 0
        }
        for k, v in topic_map.items()
    ],
    key=lambda x: x["hours"],
    reverse=True
)


# ------------------------------
# STUDY TIME AGGREGATION
# ------------------------------

def study_time(entries, mode="daily"):
    data = defaultdict(float)

    for e in entries:

        if mode == "daily":
            key = e.date.strftime("%Y-%m-%d")

        elif mode == "weekly":
            key = e.date.strftime("%A")

        elif mode == "monthly":
            key = f"Week-{(e.date.day - 1)//7 + 1}"

        else:
            key = e.date.strftime("%Y-%m")

        data[key] += e.hours

    return dict(data)


# ------------------------------
# WEEKLY PATTERN
# ------------------------------

def analyze_weekly_pattern(entries):
    day_map = defaultdict(int)

    for entry in entries:
        day = entry.date.strftime("%A")
        day_map[day] += entry.hours * 60

    if not day_map:
        return {}

    dominant_day = max(day_map, key=day_map.get)

    weekday_minutes = sum(
        v for k, v in day_map.items() if k not in ["Saturday", "Sunday"]
    )

    weekend_minutes = sum(
        v for k, v in day_map.items() if k in ["Saturday", "Sunday"]
    )

    ratio = weekday_minutes / weekend_minutes if weekend_minutes else 999

    learning_type = (
        "Weekday-focused"
        if ratio > 2
        else "Weekend warrior"
        if ratio < 0.5
        else "Balanced"
    )

    values = list(day_map.values())

    consistency_type = (
        "Burst Learner"
        if len(values) > 1 and stdev(values) > mean(values)
        else "Structured"
    )

    return {
        "dominant_day": dominant_day,
        "learning_type": learning_type,
        "consistency_type": consistency_type,
    }


# ------------------------------
# LEARNING OVERVIEW
# ------------------------------

def learning_overview(entries):
    total_tasks = len(entries)
    total_points = sum(int(e.hours * 10) for e in entries)

    return {
        "tasks_completed": total_tasks,
        "points_earned": total_points,
    }


# ------------------------------
# PRODUCTIVITY SCORE
# ------------------------------

def calculate_productivity_score(
    weekly_minutes,
    target_weekly_minutes,
    consistency_score,
    velocity_score,
    goal_completion_rate,
    streak,
    last_week_score=None
):
    minutes_score = min((weekly_minutes / target_weekly_minutes) * 100, 100)
    streak_score = min(streak * 5, 100)

    base_score = (
        0.3 * minutes_score +
        0.2 * consistency_score +
        0.2 * velocity_score +
        0.15 * goal_completion_rate +
        0.15 * streak_score
    )

    if last_week_score:
        final_score = 0.7 * base_score + 0.3 * last_week_score
    else:
        final_score = base_score
    return round(final_score, 2)


def productivity_label(score):
    if score >= 90:
        return "Elite Focus"
    elif score >= 75:
        return "High Momentum"
    elif score >= 60:
        return "Steady Progress"
    elif score >= 40:
        return "Inconsistent"
    else:
        return "Needs Structure"

# ------------------------------
# MONTHLY GOAL
# ------------------------------


def monthly_goal_progress(entries, monthly_goal_hours):

    now = datetime.utcnow()

    month_entries = [
        e for e in entries
        if e.date.month == now.month and e.date.year == now.year
    ]

    total_hours = sum(e.hours for e in month_entries)

    completion = (total_hours / monthly_goal_hours) * \
        100 if monthly_goal_hours else 0

    return {
        "hours_completed": total_hours,
        "goal": monthly_goal_hours,
        "completion_rate": round(completion, 2)
    }


def generate_insights(productivity_score, consistency_score, velocity_score):
    insights = []

    if consistency_score < 50:
        insights.append({
            "id": "low_consistency",
            "message": "Your learning pattern is irregular.",
            "recommendation": "Try fixed daily time blocks."
        })
    if velocity_score < 50:
        insights.append({
            "id": "declining_velocity",
            "message": "Your learning pace has slowed.",
            "recommendation": "Increase session duration slightly."
        })
    if productivity_score >= 80:
        insights.append({
            "id": "strong_momentum",
            "message": "You're in a strong learning phase.",
            "recommendation": "Use this momentum for complex topics."
        })
    return insights[:3]

# ------------------------------
# BADGES / ACHIEVEMENTS
# ------------------------------


def evaluate_badges(streak, total_hours, monthly_goal_completion, projects_completed):
    badges = []
    if streak >= 7:
        badges.append("7_day_streak")
    if streak >= 30:
        badges.append("30_day_streak")
    if total_hours >= 100:
        badges.append("100_hour_master")
    if monthly_goal_completion >= 120:
        badges.append("goal_crusher")
    if projects_completed >= 3:
        badges.append("project-trio")
    return badges
