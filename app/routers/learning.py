from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from uuid import UUID

from app.analytics.engine import (
    calculate_productivity_score,
    productivity_label,
    analyze_weekly_pattern,
    generate_insights,
    evaluate_badges,
    calculate_daily_streak,
    calculate_longest_streak,
    learning_velocity,
    consistency_score,
    topic_breakdown,
    study_time,
    learning_overview
)

from .. import models, schemas
from ..database import get_db

router = APIRouter()

DEMO_USER_ID = 1


# ----------------------------
# TOPICS
# ----------------------------

@router.post("/topics", response_model=schemas.TopicResponse)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):

    new_topic = models.Topic(**topic.model_dump())

    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)

    return new_topic


@router.get("/topics", response_model=list[schemas.TopicResponse])
def get_topics(db: Session = Depends(get_db)):

    return db.query(models.Topic).order_by(
        models.Topic.created_at.desc()
    ).all()


@router.delete("/topics/{topic_id}")
def delete_topic(topic_id: UUID, db: Session = Depends(get_db)):

    topic = db.query(models.Topic).filter(
        models.Topic.id == topic_id
    ).first()

    if not topic:
        raise HTTPException(404, "Topic not found")

    db.delete(topic)
    db.commit()

    return {"message": "Topic deleted"}


# ----------------------------
# SUBTOPICS
# ----------------------------

@router.post("/subtopics", response_model=schemas.SubTopicResponse)
def create_subtopic(subtopic: schemas.SubTopicCreate, db: Session = Depends(get_db)):

    topic = db.query(models.Topic).filter(
        models.Topic.id == subtopic.topic_id
    ).first()

    if not topic:
        raise HTTPException(404, "Topic not found")

    new_subtopic = models.SubTopic(**subtopic.model_dump())

    db.add(new_subtopic)
    db.commit()
    db.refresh(new_subtopic)

    return new_subtopic


@router.get("/subtopics/{topic_id}", response_model=list[schemas.SubTopicResponse])
def get_subtopics(topic_id: UUID, db: Session = Depends(get_db)):

    return db.query(models.SubTopic).filter(
        models.SubTopic.topic_id == topic_id
    ).order_by(models.SubTopic.created_at.asc()).all()


@router.put("/subtopics/{subtopic_id}/toggle", response_model=schemas.SubTopicResponse)
def toggle_subtopic(subtopic_id: UUID, db: Session = Depends(get_db)):

    subtopic = db.query(models.SubTopic).filter(
        models.SubTopic.id == subtopic_id
    ).first()

    if not subtopic:
        raise HTTPException(404, "Subtopic not found")

    subtopic.completed = not subtopic.completed

    db.commit()
    db.refresh(subtopic)

    return subtopic


# ----------------------------
# PROJECTS
# ----------------------------

@router.post("/projects", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):

    new_project = models.Project(
        user_id=DEMO_USER_ID,
        **project.model_dump()
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get("/projects", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):

    return db.query(models.Project).filter(
        models.Project.user_id == DEMO_USER_ID
    ).order_by(models.Project.created_at.desc()).all()


# ----------------------------
# LEARNING ENTRY
# ----------------------------

@router.post("/", response_model=schemas.LearningEntryResponse)
def create_entry(entry: schemas.LearningEntryCreate, db: Session = Depends(get_db)):

    new_entry = models.LearningEntry(
        user_id=DEMO_USER_ID,
        **entry.model_dump()
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


@router.get("/", response_model=list[schemas.LearningEntryResponse])
def get_entries(db: Session = Depends(get_db)):

    return db.query(models.LearningEntry).filter(
        models.LearningEntry.user_id == DEMO_USER_ID
    ).order_by(models.LearningEntry.date.desc()).all()


# ----------------------------
# MONTHLY GOAL
# ----------------------------

@router.post("/goal")
def set_monthly_goal(target_hours: float, db: Session = Depends(get_db)):

    current_month = datetime.utcnow().strftime("%Y-%m")

    goal = db.query(models.MonthlyGoal).filter(
        models.MonthlyGoal.user_id == DEMO_USER_ID,
        models.MonthlyGoal.month == current_month
    ).first()

    if goal:
        goal.target_hours = target_hours
    else:
        goal = models.MonthlyGoal(
            user_id=DEMO_USER_ID,
            month=current_month,
            target_hours=target_hours
        )
        db.add(goal)

    db.commit()

    return {"message": "Goal saved"}


# ----------------------------
# DASHBOARD ANALYTICS
# ----------------------------

@router.get("/analytics/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    entries = db.query(models.LearningEntry).filter(
        models.LearningEntry.user_id == DEMO_USER_ID
    ).order_by(models.LearningEntry.date.asc()).all()

    if not entries:
        return {"status": "success", "data": {}}

    # streaks
    daily_streak = calculate_daily_streak(entries)
    longest_streak = calculate_longest_streak(entries)

    # velocity
    velocity = learning_velocity(entries)

    # consistency
    consistency = consistency_score(entries)

    # topic breakdown
    topics = topic_breakdown(entries)

    # study time
    study = study_time(entries, "daily")

    # overview
    overview = learning_overview(entries)

    # weekly pattern
    pattern = analyze_weekly_pattern(entries)

    # productivity
    weekly_minutes = sum(e.hours * 60 for e in entries[-7:])

    productivity = calculate_productivity_score(
        weekly_minutes,
        300,
        consistency,
        velocity,
        100,
        daily_streak
    )

    insights = generate_insights(
        productivity,
        consistency,
        velocity
    )

    # project badge logic
    projects_completed = db.query(models.Project).filter(
        models.Project.user_id == DEMO_USER_ID
    ).count()

    badges = evaluate_badges(
        daily_streak,
        sum(e.hours for e in entries),
        100,
        projects_completed
    )

    return {
        "status": "success",
        "data": {
            "daily_streak": daily_streak,
            "longest_streak": longest_streak,
            "velocity": velocity,
            "consistency": consistency,
            "overview": overview,
            "topic_breakdown": topics,
            "study_time": study,
            "pattern": pattern,
            "productivity_score": productivity,
            "productivity_label": productivity_label(productivity),
            "insights": insights,
            "badges": badges
        }
    }


# ----------------------------
# STUDY TIME DROPDOWN
# ----------------------------

@router.get("/analytics/study-time")
def get_study_time(mode: str = "daily", db: Session = Depends(get_db)):

    entries = db.query(models.LearningEntry).filter(
        models.LearningEntry.user_id == DEMO_USER_ID
    ).all()

    return study_time(entries, mode)


# ----------------------------
# USER BADGES
# ----------------------------

@router.get("/badges")
def get_badges(db: Session = Depends(get_db)):

    badges = db.query(models.Badge).filter(
        models.Badge.user_id == DEMO_USER_ID
    ).all()

    return badges
