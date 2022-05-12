from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

import moe.database as database
from moe.thememanager import ThemeManager

app = FastAPI()
theme_manager = ThemeManager()


async def check_key(key, check_for_exists=False):
    if not await database.check_key(key):
        HTTPException(status_code=404, detail="Key not found")
    elif check_for_exists:
        HTTPException(status_code=403, detail="This key is already used")


async def check_password(key, password, salt=None):
    await check_key(key)
    if not await database.create_key(key, password, salt):
        HTTPException(status_code=401, detail="Wrong password")


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


@app.get("/request/themes")
async def get_themes():
    return list(theme_manager.themes.keys())


@app.post("/request/take_key")
async def post_take_key(key: str, password: str, salt: str = ""):
    await check_key(key, True)
    password_hash = await database.create_key(key, password, salt)
    if not password_hash:
        raise HTTPException(status_code=409)
    return {"detail": "This key is yours now"}


@app.delete("/request/remove_key")
async def delete_remove_key(key: str, password: str, salt: str = ""):
    await check_key(key)
    revoked = await database.revoke_key(key, password, salt)
    if not revoked:
        raise HTTPException(status_code=409, detail="Can't revoke key")
    return {"detail": "This key is free now"}


@app.get("/request/image@{key}")
async def get_image(key: str, max_length=7, lead_zeros=True, theme: str = None, do_inc=True):
    await check_key(key)
    value = await database.get_visits(key, do_inc)
    if value == -1:
        raise HTTPException(status_code=404, detail="This key not registered")
    return HTMLResponse(theme_manager.build_image(value, max_length, False, lead_zeros, theme),
                        media_type="image/svg+xml", headers={'cache-control': 'max-age=31536000'})


@app.get("/request/record@{key}")
async def get_record(key: str, do_inc=False):
    await check_key(key)
    value = await database.get_visits(key, do_inc)
    if value == -1:
        raise HTTPException(status_code=404, detail="This key not registered")
    return {"visits": value}


@app.put("/request/set@{key}")
async def patch_set(key: str, value: int, password: str, salt: str = ""):
    await check_password(key, password, salt)
    if await database.set_visits(key, value, password, salt):
        return {"detail": "Your key updated"}
    raise HTTPException(status_code=500, detail="Internal Server Error")
