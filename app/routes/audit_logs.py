from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate, AuditLogResponse

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.post(
    "/",
    response_model=AuditLogResponse,
    status_code=201,
)
def create_audit_log(
    data: AuditLogCreate,
    db: Session = Depends(get_db),
):
    log = AuditLog(**data.model_dump())

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


@router.get(
    "/",
    response_model=list[AuditLogResponse],
)
def get_audit_logs(
    db: Session = Depends(get_db),
):
    return (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )


@router.get(
    "/user/{user_id}",
    response_model=list[AuditLogResponse],
)
def get_user_audit_logs(
    user_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(AuditLog)
        .filter(AuditLog.user_id == user_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )