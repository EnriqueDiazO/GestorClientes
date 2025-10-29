
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .db import init_db
from .routers import auth, clients, reports, dashboard
from .web import router as web_router

app = FastAPI(title="Gestión de Clientes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(reports.router)
app.include_router(dashboard.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(web_router)

@app.get("/health")
def health():
    return {"ok": True}
