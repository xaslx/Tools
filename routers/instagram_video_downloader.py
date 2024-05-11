from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from tools import Tools

templater = Jinja2Templates('static/templates')

router = APIRouter(
    prefix='/download/instagram',
    tags=['Загрузчик видео с Инстаграмм']
)



@router.get('')
async def main_page(request: Request):
    return templater.TemplateResponse('instagram.html', {'request': request})

@router.post('')
async def download_video(link: str = Form()):
    return await Tools.download_video_inst(link)
    