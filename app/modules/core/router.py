"""
Core Router — System Core
==========================
Endpoints administrativos do Vyron System:
  - GET /audit-logs  →  Consulta os logs de auditoria (últimos N registros)
"""

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Core"])


@router.get("/audit-logs", response_model=List[schemas.AuditLogResponse])
def list_audit_logs(
    limit: int = Query(default=50, ge=1, le=500, description="Quantidade de registros"),
    db: Session = Depends(get_db),
):
    """Retorna os últimos registros de auditoria ordenados por timestamp DESC."""
    logs = (
        db.query(models.AuditLog)
        .order_by(models.AuditLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return logs
