from fastapi import APIRouter, Request, Form, Body
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from tiktok_downloader import ttdownloader
import secrets
from io import BytesIO, BufferedWriter

templater = Jinja2Templates('static/templates')

router = APIRouter(
    prefix='/download/tiktok',
    tags=['Загрузчик видео с тик ток']
)


@router.get('')
async def get_main_page(request: Request):
    return templater.TemplateResponse('tiktok.html', {'request': request})

@router.post('')
async def download_video(link: str = Form(...)):
    try:
        video = ttdownloader(link)
    except ValueError:
        raise HTTPException(status_code=404, detail='Видео не найдено, или неверная ссылка')
    buffer = BytesIO()
    writer = BufferedWriter(buffer)
    video[0].download(writer)
    buffer.seek(0)
    return StreamingResponse(iter([buffer.getvalue()])) 