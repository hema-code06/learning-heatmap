from datetime import datetime
from statistics import mean, stdev
from collections import defaultdict


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
        final_score = 0.7*base_score+0.3*last_week_score
    else:
        final_score(final_score, 2)


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


def analyze_weekly_pattern(entries):
    day_map = defaultdict(int)
    for entry in entries:
        day = entry.created_at.strftime("%A")
        day_map[day] += entry.duration

    if not day_map:
        return {}

    dominant_day = max(day_map, key=day_map.get)
    weekday_minutes = sum(v for k, v in day_map.items()
                          if k not in ["Saturday", "Sunday"])
    weekend_minutes = sum(v for k, v in day_map.items()
                          if k in ["Saturday", "Sunday"])
    ratio = weekday_minutes / weekend_minutes if weekend_minutes > 0 else 999

    learning_type = "Weekday-focused" if ratio > 2 else "Weekend warrior" if ratio < 0.5 else "Balanced"
    values = list(day_map.values())
    consistency_type = "Burst Learner" if len(values) > 1 and stdev(
        values) > mean(values) else "Structured"

    return {
        "dominant_day": dominant_day,
        "learning_type": learning_type,
        "consistency_type": consistency_type
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

def evaluate_badges(streak, total_hours, monthly_goal_completion):
    badges = []
    if streak >= 7:
        badges.append("7_day_streak")
    if streak >=30:
        badges.append("30_day_streak")
    if total_hours >=100:
        badges.append("100_hour_master")
    if monthly_goal_completion >= 120:
        badges.append("goal_crusher")
    return badges
