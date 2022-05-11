from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

import moe.database as database
from moe.thememanager import ThemeManager

app = FastAPI()
theme_manager = ThemeManager()


@app.on_event("startup")
async def on_startup():
    await database.sync()


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


@app.post("/request/take_key")
async def post_take_key(key: str, password: str, salt: str = ""):
    password_hash = await database.create_key(key, password, salt)
    if not password_hash:
        raise HTTPException(status_code=409)
    return {"detail": "This key is your now!"}


@app.delete("/request/remove_key")
async def delete_remove_key(key: str, password: str, salt: str = ""):
    revoked = await database.revoke_key(key, password, salt)
    if not revoked:
        raise HTTPException(status_code=409, detail="Can't revoke key, may be its already deleted?")
    return {"detail": "This key is free now!"}


@app.get("/request/@{key}")
async def get_key(key: str, max_length=7, lead_zeros=True, theme: str = None, do_inc=True):
    value = await database.get_visits(key, do_inc)
    if value == -1:
        raise HTTPException(status_code=404, detail="This key not registered!")
    return HTMLResponse(theme_manager.build_image(value, max_length, False, lead_zeros, theme),
                        media_type="image/svg+xml", headers={'cache-control': 'max-age=31536000'})
