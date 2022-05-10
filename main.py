from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import moe.utils


app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("index.html", media_type="text/html")


@app.get("/number/{number}")
async def number(number: int, theme: str = "asoul", length: int = 7, zeros: bool = True):
    return HTMLResponse(moe.utils.get_count_image(number, theme, length, zeros), media_type="image/svg+xml", headers={'cache-control': 'max-age=31536000'})
