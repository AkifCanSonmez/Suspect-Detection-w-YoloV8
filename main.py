import sys
sys.path.append("..")

from fastapi import FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from routers import home
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key="asdf3r34a")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(home.router)
