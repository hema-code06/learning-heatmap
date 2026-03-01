from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta
from uuid import UUID

from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.LearningEntryResponse)
def create_entry(
    entry: schemas.LearningEntryCreate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user)
):
    new_entry = models.LearningEntry(
        user_id=user_id,
        **entry.model_dump()
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


@router.get("/", response_model=list[schemas.LearningEntryResponse])
def get_entries(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):

    results = db.query(models.LearningEntry).filter(
        models.LearningEntry.user_id == user_id
    ).order_by(models.LearningEntry.date.desc()).all()
    
    return results


@router.put("/{entry_id}", response_model=schemas.LearningEntryResponse)
def update_entry(
    entry_id: UUID,
    updated_data: schemas.LearningEntryUpdate,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user)
):
    entry = db.query(models.LearningEntry).filter(
        models.LearningEntry.id == entry_id,
        models.LearningEntry.user_id == user_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found!")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    db.commit()
    db.refresh(entry)

    return entry


@router.delete("/{entry_id}")
def delete_entry(
    entry_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user)
):
    entry = db.query(models.LearningEntry).filter(
        models.LearningEntry.id == entry_id,
        models.LearningEntry.user_id == user_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found!")

    db.delete(entry)
    db.commit()

    return {"message": "Entry deleted successfully"}


@router.get("/heatmap")
def get_heatmap(
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user)
):
    results = db.query(
        models.LearningEntry.date,
        func.sum(models.LearningEntry.hours).label("total_hours")
    ).filter(
        models.LearningEntry.user_id == user_id
    ).group_by(
        models.LearningEntry.date
    ).all()

    if not results:
        return []

    data_dict = {r.date: r.total_hours for r in results}
    start = min(data_dict.keys())
    end = max(data_dict.keys())

    filled = []
    current = start

    while current <= end:
        filled.append({
            "date": current,
            "total_hours": data_dict.get(current, 0)
        })
        current += timedelta(days=1)

    return filled
