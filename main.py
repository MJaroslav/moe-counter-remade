from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from starlette.staticfiles import StaticFiles

import moe.database as database
from moe.thememanager import ThemeManager

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
theme_manager = ThemeManager()


async def check_key(key, check_for_exists=False):
    if not await database.check_key(key):
        if not check_for_exists:
            raise HTTPException(status_code=404, detail="Key not found")
    elif check_for_exists:
        raise HTTPException(status_code=403, detail="This key is already used")


async def check_password(key, password, salt):
    await check_key(key)
    if not await database.check_password(key, password, salt):
        raise HTTPException(status_code=401, detail="Wrong password")


@app.on_event("startup")
async def on_startup():
    await database.sync()


@app.get("/", include_in_schema=False)
async def get_root():
    return FileResponse("index.html", media_type="text/html")


@app.get("/request/number")
async def get_number(value: int, max_length: int = 7, lead_zeros: bool = False,
                     theme: str = None, smoothing: bool = False):
    """
    Generate image for any number.
    :param value: Number for generate.
    :param max_length: Maximum number of digits in result image (Eg for value 123 and max_length 2 answer will be 23).
    Use zero for disable.
    :param lead_zeros: Adds extra zeros to left of value if its length less than max_length.
    :param theme: Image set for numbers. For wrong values default theme will be used.
    :param smoothing Do image smoothing.
    :return: Generated image from params with one year max cache age.
    """
    return HTMLResponse(theme_manager.build_image(value, max_length, False, lead_zeros, theme, smoothing),
                        media_type="image/svg+xml", headers={'cache-control': 'max-age=31536000'})


@app.get("/request/demo")
async def get_demo(theme: str = None, smoothing: bool = False):
    """
    Generate image for theme demonstration.
    :param theme: Image set for numbers. For wrong values default theme will be used.
    :param smoothing Do image smoothing.
    :return: Generated image from params with one year max cache age.
    """
    return HTMLResponse(theme_manager.build_image(demo=True, theme=theme, smoothing=smoothing),
                        media_type="image/svg+xml",
                        headers={'cache-control': 'max-age=31536000'})


@app.get("/request/themes")
async def get_themes():
    """
    Get list of available themes.
    :return: List of themes in json array format.
    """
    return list(theme_manager.themes.keys())


@app.post("/request/take_key")
async def post_take_key(key: str, password: str, salt: str = ""):
    """
    Register key for counter (this allows you edit value and delete this key in future).
    :param key: Unique name for key.
    :param password: Your key password (don't forget this if you don't want to lose access to your key!)
    :param salt: Additional salt for password (don't forget this if you don't want to lose access to your key!)
    :return: Code 200 if success.
    """
    await check_key(key, True)
    password_hash = await database.create_key(key, password, salt)
    if not password_hash:
        raise HTTPException(status_code=409)
    return {"detail": "This key is yours now"}


@app.delete("/request/revoke_key")
async def delete_remove_key(key: str, password: str, salt: str = ""):
    """
    Delete your counter key (all links to this counter will be break and anyone can register this key again).
    :param key: Key for deleting.
    :param password: Password of key.
    :param salt: Salt for password of key.
    :return: Code 200 if success.
    """
    await check_password(key, password, salt)
    revoked = await database.revoke_key(key, password, salt)
    if not revoked:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"detail": "This key is free now"}


@app.get("/request/image@{key}")
async def get_image(key: str, max_length: int = 7, lead_zeros: bool = True, theme: str = None, do_inc: bool = True,
                    smoothing: bool = False):
    """
    Generate image for counter.
    :param key: Any registered counter key.
    :param max_length: Maximum number of digits in result image (Eg for value 123 and max_length 2 answer will be 23).
    Use zero for disable.
    :param lead_zeros: Adds extra zeros to left of value if its length less than max_length.
    :param theme: Image set for numbers. For wrong values default theme will be used.
    :param do_inc: Do increment for counter by this request.
    :param smoothing Do image smoothing.
    :return: Generated image of counter with their current value none zero cache age.
    """
    await check_key(key)
    value = await database.get_visits(key, do_inc)
    if value == -1:
        raise HTTPException(status_code=404, detail="This key not registered")
    return HTMLResponse(theme_manager.build_image(value, max_length, False, lead_zeros, theme, smoothing),
                        media_type="image/svg+xml",
                        headers={'cache-control': 'max-age=0, no-cache, no-store, must-revalidate'})


@app.get("/request/record@{key}")
async def get_record(key: str, do_inc: bool = False):
    """
    Return data of counter.
    :param key: Any registered counter key.
    :param do_inc: Do increment for counter by this request.
    :return: counter info in json format (object with "visits" field).
    """
    await check_key(key)
    value = await database.get_visits(key, do_inc)
    if value == -1:
        raise HTTPException(status_code=404, detail="This key not registered")
    return {"visits": value}


@app.put("/request/set@{key}", status_code=201)
async def patch_set(key: str, value: int, password: str, salt: str = ""):
    """
    Change value of counter.
    :param key: Any registered counter key.
    :param value: New value for counter.
    :param password: Password of key.
    :param salt: Salt for password of key.
    :return: Code 201 if success.
    """
    await check_password(key, password, salt)
    if await database.set_visits(key, value, password, salt):
        return {"detail": "Your key updated"}
    raise HTTPException(status_code=500, detail="Internal Server Error")
