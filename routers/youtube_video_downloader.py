from fastapi import APIRouter, Request, Form
from fastapi.responses import StreamingResponse

from fastapi.templating import Jinja2Templates
from tools import Tools

templates = Jinja2Templates('static/templates')

router = APIRouter(
    prefix='/download/youtube',
    tags=['Загрузчик видео с YouTube']
)



@router.get('')
async def get_main_page(request: Request):
    return templates.TemplateResponse('youtube.html', {'request': request})



@router.post('', response_class=StreamingResponse)
async def download_video(link: str = Form(), resolution: str = Form()):
    return await Tools.download_video_yt(link, resolution)


