from fastapi import APIRouter, Request, Body, File, UploadFile
from fastapi.templating import Jinja2Templates
import segno
import secrets
import aiofiles
import aiofiles.os
from typing import Annotated
import cv2
from fastapi.responses import JSONResponse
import json
from json.decoder import JSONDecodeError



templates = Jinja2Templates('static/templates')

router = APIRouter(
    prefix='/qrcode',
    tags=['Генерация qr кода']
)




@router.get('')
async def get_qr_code_page(request: Request):
    return templates.TemplateResponse('generate_qrcode.html', {'request': request})

@router.get('/scan')
async def get_qr_code_img(request: Request):
    return templates.TemplateResponse('scan_qrcode.html', {'request': request})

@router.post('/scan')
async def scan_qr_code(image: Annotated[UploadFile, File()]):


    extension: str = image.filename.split('.')[-1]

    if extension not in ['jpg', 'png']:
        return JSONResponse(content={'msg': 'Расширение файла должно быть (jpg или png)'})
    
    FILEPATH: str = "static/scan/"
    token_name: str = secrets.token_hex(10) + "." + extension
    generated_name: str = FILEPATH + token_name


    async with aiofiles.open(generated_name, "wb") as file:
        content = await image.read()
        await file.write(content)
        
    
    img = cv2.imread(generated_name)
    try:
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
    except Exception:
        data = ''
    try:
        data = json.loads(data)
    except JSONDecodeError:
        data = ''
    await aiofiles.os.remove(generated_name)
    if len(data) > 0:
        return {'data': data['link']}
    
    return JSONResponse(content={'msg': 'Qr Code не обнаружен'})

@router.post('')
async def create_qr_code(link: str = Body()):
    qrcode = segno.make_qr(link)
    filename: str = secrets.token_hex(10) + '.png'
    qrcode.save(
        f'static/image/{filename}',
        scale=7,
        light="lightgray",
    )
    return {'image_url': f'static/image/{filename}'}
