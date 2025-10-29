
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..auth import require_role
from ..db import get_session
from ..models import Client, Document, Role

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/client/{client_id}", dependencies=[Depends(require_role(Role.ADMIN_1, Role.ADMIN_2))])
def client_report(client_id: int, session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        return {"exists": False}
    docs = session.exec(select(Document).where(Document.client_id == client_id)).all()
    return {
        "exists": True,
        "client": client,
        "documents": [{"filename": d.filename, "uploaded_at": d.uploaded_at} for d in docs],
    }
