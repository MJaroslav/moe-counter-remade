from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

from moe.thememanager import ThemeManager

app = FastAPI()
theme_manager = ThemeManager()


@app.get("/")
async def get_root():
    return FileResponse("index.html", media_type="text/html")


@app.get("/request/number")
async def get_number(value: int, max_length: int = 7, lead_zeros: bool = False,
                     theme: str = None):
    return HTMLResponse(theme_manager.build_image(value, max_length, False, lead_zeros, theme),
                        media_type="image/svg+xml", headers={'cache-control': 'max-age=31536000'})


@app.get("/request/demo")
async def get_demo(theme: str = None):
    return HTMLResponse(theme_manager.build_image(demo=True, theme=theme), media_type="image/svg+xml",
                        headers={'cache-control': 'max-age=31536000'})
