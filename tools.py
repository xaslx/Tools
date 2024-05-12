from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from tiktok_downloader import ttdownloader
from io import BytesIO, BufferedWriter
from pytube import YouTube
from fastapi.responses import StreamingResponse
from pytube.exceptions import RegexMatchError, VideoUnavailable
from instagrapi import Client
from fastapi.responses import StreamingResponse
import aiohttp
from dotenv import load_dotenv
import os


load_dotenv()
login: str = os.environ.get('LOGIN_INST')
password: str = os.environ.get('PASSWORD_INST')
cl = Client()
cl.login(login, password)



class Tools:

    @classmethod
    async def download_video_tt(cls, link: str) -> StreamingResponse:
        try:
            video = ttdownloader(link)
        except ValueError:
            raise HTTPException(status_code=404, detail='Видео не найдено, или неверная ссылка')
        buffer: BytesIO = BytesIO()
        writer: BufferedWriter = BufferedWriter(buffer)
        video[0].download(writer)
        buffer.seek(0)
        return StreamingResponse(iter([buffer.getvalue()])) 
    
    @classmethod
    async def download_video_yt(cls, link: str, resolution: str) -> StreamingResponse:
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
    
    @classmethod
    async def download_video_inst(cls, link: str) -> StreamingResponse:
        async with aiohttp.ClientSession() as session:
            res = cl.media_pk_from_url(link)
            video_url = str(cl.media_info(res).video_url)
        
            async with session.get(video_url) as resp:
                if resp.status == 200:
                    video_stream = await resp.content.read()
                    return StreamingResponse(BytesIO(video_stream), media_type='video/mp4')
                else:
                    return {'msg': 'Видео не найдено'}