from fastapi import APIRouter, HTTPException, Request, Form
from pytube import YouTube
from fastapi.responses import StreamingResponse

from fastapi.templating import Jinja2Templates

from pytube.exceptions import RegexMatchError, VideoUnavailable
from io import BytesIO


templates = Jinja2Templates('static/templates')

router = APIRouter(
    prefix='/download/youtube',
    tags=['Загрузчик видео с YouTube']
)



@router.get('')
async def get_main_page(request: Request):
    return templates.TemplateResponse('youtube.html', {'request': request})



@router.post('', response_class=StreamingResponse)
async def download_video(link: str = Form(...), resolution: str = Form(...)):
    try:
        yt: YouTube = YouTube(link)
    except (RegexMatchError, VideoUnavailable) as e:
        raise HTTPException(status_code=404, detail='Видео не найдено или недоступно!')

    if resolution == 'highest':
        video = yt.streams.get_highest_resolution()
    elif resolution == 'lowest':
        video = yt.streams.get_lowest_resolution()

    if video.filesize > 524288000:
        raise HTTPException(status_code=413, detail='Видео не может быть больше 500мб')
    
    buffer: BytesIO = BytesIO()
    video.stream_to_buffer(buffer)
    buffer.seek(0)

    return StreamingResponse(iter([buffer.getvalue()]), media_type='video/mp4')


