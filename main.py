from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routers.images import router as image_router
from routers.qrcode import router as qrcode_router
from routers.youtube_video_downloader import router as youtube_router
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


templates = Jinja2Templates('static/templates')

app = FastAPI(title='ai Image')


app.mount("/static", StaticFiles(directory="static"), "static")

app.include_router(image_router)
app.include_router(qrcode_router)
app.include_router(youtube_router)

@app.get('/')
async def main_page(request: Request):
    return templates.TemplateResponse('main_page.html', {'request': request})


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)