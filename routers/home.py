import sys
sys.path.append("..")

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import FileResponse
import imageio.v3 as iio
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import io
import uuid

from detect import detect_human
from utils_common import collect_frames_w_suspects, generate_video



templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="",
    tags=["/home"],
    responses={401: {"user": "Not authorized"}}
)

def get_session_id(request: Request):
    session_id = request.session.get("session_id")
    if session_id is None:
        session_id = str(uuid.uuid4())
        request.session["session_id"] = session_id
    return session_id

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.post("/detect-thief")
async def detect_thief(request: Request):
    session_id = get_session_id(request)
    form_data = await request.form()
    video_bytes = await form_data["video_file"].read()
    frames = iio.imread(video_bytes, index=None, format_hint=".webm")
    
    frame_list = collect_frames_w_suspects(frames)
    generate_video(frame_list, session_id)
    return templates.TemplateResponse("download-page.html", {"request": request, "session_id": session_id})

@router.get("/download")
async def download(request: Request):
    session_id = get_session_id(request)
    video_path = f"{session_id}.mp4"  # Video dosyasının yolunu belirtin
    return FileResponse(video_path, headers={"Content-Disposition": f'attachment; filename={session_id}.mp4'})
