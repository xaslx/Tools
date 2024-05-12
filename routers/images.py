from fastapi import APIRouter, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
from typing import Annotated
import os
from fusion_brain import Text2ImageAPI
import base64
import aiofiles
import secrets


load_dotenv()

api_key: str = os.environ.get('api_key')
secret_key: str = os.environ.get('secret_key')


api = Text2ImageAPI('https://api-key.fusionbrain.ai/', api_key=api_key, secret_key=secret_key)
model_id = api.get_model()



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
    image_name: str = secrets.token_hex(10)
    try:
        res: str = api.generate(body['textarea'], model_id)
        image: str = api.check_generation(res)
    except:
        raise HTTPException(status_code=500, detail='Сервер не отвечает')
    image_base64: str = image[0]
    image_data: str = base64.b64decode(image_base64)
    async with aiofiles.open(f'static/gen_image/{image_name}.webp', "wb") as file:
        await file.write(image_data)
    return {'image_url': f'static/gen_image/{image_name}.webp'}
