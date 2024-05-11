from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from tools import Tools

templater = Jinja2Templates('static/templates')

router = APIRouter(
    prefix='/download/tiktok',
    tags=['Загрузчик видео с Тик Ток']
)


@router.get('')
async def get_main_page(request: Request):
    return templater.TemplateResponse('tiktok.html', {'request': request})

@router.post('')
async def download_video(link: str = Form()):
    return await Tools.download_video_tt(link=link)