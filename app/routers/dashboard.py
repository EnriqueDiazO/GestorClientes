
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from ..auth import require_role
from ..db import get_session
from ..models import Client, Document, Role

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/kpis", dependencies=[Depends(require_role(Role.ADMIN_2))])
def kpis(session: Session = Depends(get_session)):
    total_clients = session.exec(select(func.count()).select_from(Client)).one()
    total_docs = session.exec(select(func.count()).select_from(Document)).one()
    latest_upload = session.exec(select(Document).order_by(Document.uploaded_at.desc())).first()
    return {
        "total_clients": total_clients,
        "total_documents": total_docs,
        "last_upload": getattr(latest_upload, "uploaded_at", None),
    }
