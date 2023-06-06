from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from starlette.responses import Response

app = FastAPI()

templates = Jinja2Templates(directory='templates')
CHUNK_SIZE = 1024 * 1024


@app.get('/v/{page}')
async def main(request: Request, page: int):
    return templates.TemplateResponse('index.html', {'request': request, 'page': page})


@app.get("/video/{n}")
async def video_endpoint(n: int, range: str = Header(None)):
    print(f"call{n}")
    if not n:
        return HTTPException(status_code=400, detail="Wrong parameter")
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    video_path = Path(f"v/v{n}")
    print(video_path)
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")
