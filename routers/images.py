from fastapi import APIRouter, Request, Body
from fastapi.templating import Jinja2Templates
import replicate
from dotenv import load_dotenv, get_key
from typing import Annotated
import time

load_dotenv('.env')

REPLICATE_API_TOKEN: str = get_key('.env', 'REPLICATE_API_TOKEN')


templates = Jinja2Templates('static/templates')


router = APIRouter(
    prefix='/image',
    tags=['Генерация изображения']
)

@router.get('')
async def images(request: Request):
    return templates.TemplateResponse('generate_image.html', {'request': request})

@router.post('')
async def images(body: Annotated[dict, Body()]):
    # res = replicate.run('stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
    #                             input={
    #                                 'width': int(body['width']),
    #                                 'height': int(body['height']),
    #                                 'prompt': body['textarea']
    #                             })
    res = 'https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663219930_12-mykaleidoscope-ru-p-rasteniya-dlya-yaponskogo-sada-krasivo-15.jpg'
    time.sleep(2)
    return {'image_url': res}
