
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/client", response_class=HTMLResponse)
def client_page(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})

@router.get("/admin1", response_class=HTMLResponse)
def admin1_page(request: Request):
    return templates.TemplateResponse("admin1.html", {"request": request})

@router.get("/admin2", response_class=HTMLResponse)
def admin2_page(request: Request):
    return templates.TemplateResponse("admin2.html", {"request": request})
