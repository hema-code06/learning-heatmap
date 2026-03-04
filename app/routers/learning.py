from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import timedelta, datetime
from uuid import UUID

from app.analytics.engine import (
    calculate_productivity_score,
    productivity_label,
    analyze_weekly_pattern,
    generate_insights,
    evaluate_badges
)

from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.LearningEntryResponse)
def create_entry(
    entry: schemas.LearningEntryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    data = entry.model_dump
    purpose = data.pop("purpose")
    project = data.pop("project")

    new_entry = models.LearningEntry(
        user_id=current_user.id,
        **data,
        **purpose,
        **project
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.get("/", response_model=list[schemas.LearningEntryResponse])
def get_entries(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    offset = (page-1)*limit

    results = db.query(models.LearningEntry).filter(
        models.LearningEntry.user_id == current_user.id
    ).order_by(models.LearningEntry.date.desc()).offset(offset).limit(limit).all()

    return results


@router.put("/{entry_id}", response_model=schemas.LearningEntryResponse)
def update_entry(
    entry_id: UUID,
    updated_data: schemas.LearningEntryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    entry = db.query(models.LearningEntry).filter(
        models.LearningEntry.id == entry_id,
        models.LearningEntry.user_id == current_user.id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found!")
    update_data = updated_data.model_dump(exclude_unset=True)

    if "purpose" in update_data:
        for k, v in update_data["purpose"].items():
            setattr(entry, k, v)
        update_data.pop("purpose")

    if "project" in update_data:
        for k, v in update_data["project"].items():
            setattr(entry, k, v)
        update_data.pop("project")

    for key, value in update_data.items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}")
def delete_entry(
    entry_id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    entry = db.query(models.LearningEntry).filter(
        models.LearningEntry.id == entry_id,
        models.LearningEntry.user_id == current_user.id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found!")

    db.delete(entry)
    db.commit()
    return {"message": "Entry deleted successfully"}


@router.get("/analytics/streak")
def get_weekly_streak(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    results = db.query(
        extract("year", models.LearningEntry.date).label("year"),
        extract("week", models.LearningEntry.date).label("week")
    ).filter(
        models.LearningEntry.user_id == current_user.id
    ).group_by("year", "week").order_by("year", "week").all()

    if not results:
        return {"weekly_streak": 0}

    weeks = [(int(r.year), int(r.week)) for r in results]
    streak = max_streak = 1

    for i in range(1, len(weeks)):
        prev = weeks[i-1]
        curr = weeks[i]

        if (curr[0] == prev[0] and curr[1] == prev[1] + 1):
            streak += 1
        else:
            streak = 1

        max_streak = max(max_streak, streak)

    return {"weekly_streak": max_streak}


@router.get("/analytics/velocity")
def get_learning_velocity(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    four_weeks_ago = datetime.utcnow().date() - timedelta(weeks=4)
    results = db.query(
        func.sum(models.LearningEntry.hours)
    ).filter(
        models.LearningEntry.user_id == current_user.id,
        models.LearningEntry.date >= four_weeks_ago
    ).scalar()

    total_hours = results or 0
    velocity = total_hours/4

    return {
        "weekly_average_hours_last_4_weeks": round(velocity, 2)
    }


@router.get("/analytics/consistency")
def get_consistency_score(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    results = db.query(
        func.count(func.distinct(models.LearningEntry.date))
    ).filter(
        models.LearningEntry.user_id == current_user.id,
        models.LearningEntry.date >= thirty_days_ago
    ).scalar()

    active_days = results or 0
    score = (active_days / 30)*100
    return {
        "consistency_score_percent": round(score, 2)
    }


@router.get("/analytics/velocity-trend")
def get_velocity_trend(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    results = db.query(
        extract("year", models.LearningEntry.date).label("year"),
        extract("week", models.LearningEntry.date).label("week"),
        func.sum(models.LearningEntry.hours).label("total_hours")
    ).filter(
        models.LearningEntry.user_id == current_user.id
    ).group_by(
        "year", "week"
    ).order_by(
        "year", "week"
    ).all()

    data = [
        {
            "week": f"{int(r.year)}-W{int(r.week)}",
            "hours": float(r.total_hours)
        }
        for r in results
    ]

    return data


@router.get("/analytics/topic-breakdown")
def get_topic_breakdown(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    results = db.query(
        models.LearningEntry.topic,
        func.sum(models.LearningEntry.hours).label("total_hours")
    ).filter(
        models.LearningEntry.user_id == current_user.id
    ).group_by(
        models.LearningEntry.topic
    ).order_by(
        func.sum(models.LearningEntry.hours).desc()
    ).all()

    return [
        {
            "topic": r.topic,
            "hours": float(r.total_hours)
        }
        for r in results
    ]


@router.post("/goal")
def set_monthly_goal(
    target_hours: float,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    current_month = datetime.utcnow().strftime("%Y-%m")

    existing = db.query(models.MonthlyGoal).filter(
        models.MonthlyGoal.user_id == current_user.id,
        models.MonthlyGoal.month == current_month,
    ).first()

    if existing:
        existing.target_hours = target_hours
    else:
        new_goal = models.MonthlyGoal(
            user_id=current_user.id,
            month=current_month,
            target_hours=target_hours
        )
        db.add(new_goal)

    db.commit()
    return {"message": "Goal saved successfully.."}


@router.get("/goal/progress")
def get_goal_progress(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    current_month = datetime.utcnow().strftime("%Y-%m")

    goal = db.query(models.MonthlyGoal).filter(
        models.MonthlyGoal.user_id == current_user.id,
        models.MonthlyGoal.month == current_month,
    ).first()

    if not goal:
        return {"target": 0, "completed": 0, "percentage": 0}

    month_start = datetime.utcnow().replace(day=1).date()

    total_hours = db.query(
        func.sum(models.LearningEntry.hours)
    ).filter(
        models.LearningEntry.user_id == current_user.id,
        models.LearningEntry.date >= month_start
    ).scalar() or 0

    percentage = (total_hours/goal.target_hours) * \
        100 if goal.target_hours else 0

    return {
        "target": goal.target_hours,
        "completed": round(total_hours, 2),
        "percentage": round(percentage, 2)
    }


@router.get("/analytics")
def get_advanced_analytics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    entries = db.query(models.LearningEntry).filter(
        models.LearningEntry.user_id == current_user.id
    ).order_by(models.LearningEntry.date.asc()).all()

    if not entries:
        return {
            "status": "success",
            "data": {
                "productivity_score": 0,
                "label": "No Data",
                "pattern": {},
                "insights": [],
                "badges": []
            }
        }

    # ---- Weekly Minutes (Last 7 Days) ----
    today = datetime.utcnow().date()
    # Weekly Minutes
    seven_days_ago = today - timedelta(days=7)
    weekly_entries = [e for e in entries if e.date >= seven_days_ago]
    weekly_minutes = sum(e.hours * 60 for e in weekly_entries)
    target_weekly_minutes = 300

    # Velocity
    four_weeks_ago = today - timedelta(weeks=4)
    last_4_weeks_entries = [e for e in entries if e.date >= four_weeks_ago]
    total_hours_4w = sum(e.hours for e in last_4_weeks_entries)
    velocity_score = min((total_hours_4w / 20) * 100, 100)

    # Consistency
    thirty_days_ago = today - timedelta(days=30)
    active_days = len({e.date for e in entries if e.date >= thirty_days_ago})
    consistency_score = (active_days / 30) * 100

    # Goal Completion
    current_month = today.strftime("%Y-%m")
    goal = db.query(models.MonthlyGoal).filter(
        models.MonthlyGoal.user_id == current_user.id,
        models.MonthlyGoal.month == current_month
    ).first()

    month_start = today.replace(day=1)
    month_hours = sum(e.hours for e in entries if e.date >= month_start)

    goal_completion_rate = (
        (month_hours / goal.target_hours) * 100
        if goal and goal.target_hours else 0
    )

    # Streak
    date_set = sorted({e.date for e in entries})
    streak = 1
    max_streak = 1

    for i in range(1, len(date_set)):
        if (date_set[i] - date_set[i-1]).days == 1:
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)

    score = calculate_productivity_score(
        weekly_minutes=weekly_minutes,
        target_weekly_minutes=target_weekly_minutes,
        consistency_score=consistency_score,
        velocity_score=velocity_score,
        goal_completion_rate=goal_completion_rate,
        streak=max_streak
    )

    pattern = analyze_weekly_pattern(entries)
    insights = generate_insights(score, consistency_score, velocity_score)
    calculated_badges = evaluate_badges(
        max_streak, month_hours, goal_completion_rate)

    # Persist Badges
    existing_badges = db.query(models.Badge).filter(
        models.Badge.user_id == current_user.id
    ).all()

    existing_names = {b.badge_name for b in existing_badges}

    for badge_name in calculated_badges:
        if badge_name not in existing_names:
            db.add(models.Badge(
                user_id=current_user.id,
                badge_name=badge_name
            ))

    db.commit()

    final_badges = db.query(models.Badge).filter(
        models.Badge.user_id == current_user.id
    ).all()

    return {
        "status": "success",
        "data": {
            "productivity_score": score,
            "label": productivity_label(score),
            "pattern": pattern,
            "insights": insights,
            "badges": [b.badge_name for b in final_badges]
        }
    }


@router.get("/analytics/daily-streak")
def get_daily_streak(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    dates = db.query(models.LearningEntry.date).filter(
        models.LearningEntry.user_id == current_user.id
    ).distinct().order_by(models.LearningEntry.date.asc()).all()

    if not dates:
        return {
            "current_streak": 0,
            "longest_streak": 0
        }

    date_list = [d[0] for d in dates]

    longest = 1
    current = 1

    for i in range(1, len(date_list)):
        if (date_list[i] - date_list[i-1]).days == 1:
            current += 1
        else:
            current = 1
        longest = max(longest, current)

    # Calculate current streak from today backwards
    today = datetime.utcnow().date()
    current_streak = 0
    check_day = today

    date_set = set(date_list)

    while check_day in date_set:
        current_streak += 1
        check_day -= timedelta(days=1)

    return {
        "current_streak": current_streak,
        "longest_streak": longest
    }


@router.get("/badges")
def get_user_badges(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    badges = db.query(models.Badge).filter(
        models.Badge.user_id == current_user.id
    ).order_by(models.Badge.unlocked_at.desc()).all()

    return [
        {
            "name": b.badge_name,
            "unlocked_at": b.unlocked_at
        }
        for b in badges
    ]
