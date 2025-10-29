
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session, select
from ..auth import require_role
from ..db import get_session
from ..models import Client, Document, Role
from ..config import settings
import os, shutil

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/register", dependencies=[Depends(require_role(Role.CLIENTE, Role.ADMIN_1, Role.ADMIN_2))])
def register_client(
    nombre: str = Form(...),
    telefono: str = Form(""),
    user = Depends(require_role(Role.CLIENTE, Role.ADMIN_1, Role.ADMIN_2)),
    session: Session = Depends(get_session)
):
    client = Client(user_id=user.id, nombre=nombre, telefono=telefono)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@router.post("/{client_id}/upload", dependencies=[Depends(require_role(Role.CLIENTE, Role.ADMIN_1, Role.ADMIN_2))])
async def upload_document(client_id: int, file: UploadFile = File(...), session: Session = Depends(get_session)):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    dest = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    doc = Document(client_id=client_id, filename=file.filename, stored_path=dest, content_type=file.content_type)
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return {"ok": True, "document": doc}

@router.get("/{client_id}/documents", dependencies=[Depends(require_role(Role.ADMIN_1, Role.ADMIN_2))])
def list_documents(client_id: int, session: Session = Depends(get_session)):
    docs = session.exec(select(Document).where(Document.client_id == client_id)).all()
    return docs
