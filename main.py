from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routers.images import router as image_router
from routers.qrcode import router as qrcode_router
from routers.youtube_video_downloader import router as youtube_router
from routers.tiktok_video_downloader import router as tiktok_router
from routers.instagram_video_downloader import router as instagram_router
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException


templates = Jinja2Templates('static/templates')

app = FastAPI(title='Tools')


app.mount('/static', StaticFiles(directory='static'), 'static')

app.include_router(image_router)
app.include_router(qrcode_router)
app.include_router(youtube_router)
app.include_router(tiktok_router)
app.include_router(instagram_router)


@app.get('/')
async def main_page(request: Request):
    return templates.TemplateResponse('main_page.html', {'request': request})

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse('/')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)