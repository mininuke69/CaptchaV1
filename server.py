from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import Response
from secrets import token_urlsafe
from io import BytesIO
from typing import List
from json import loads

from stablelib import generate_captcha

app = FastAPI()
current_captchas = {}


@app.get("/")
async def home(r: Request):
    return FileResponse("web/html/index.html")


@app.get("/captcha")
async def embed(r: Request, token: str | None = None):
    global current_captchas
    
    captcha_key = token_urlsafe()
    img, solution = generate_captcha()
    current_captchas[captcha_key] = "".join([str(s) for s in solution])

    b = BytesIO()
    img.save(b, format="PNG")
    
    return Response(b.getvalue(), media_type="image/png", headers={"X-Captcha-Key": captcha_key})


@app.post("/verify")
async def verify(r: Request):
    global current_captchas
    body_bytes = await r.body()
    body = loads(body_bytes.decode())

    print(body)
    
    captcha_key = body["captcha_key"]
    solution = body["solution"]
    try:
        if str(current_captchas[captcha_key]) == str(solution):
            # we should delete it, but it's causing problems, so nope
            current_captchas.pop(captcha_key)
            return True
        else:
            return False
    except KeyError:
        return {"error": "captcha key does not exist"}




if __name__ == "__main__":
    from uvicorn import run
    run("server:app")