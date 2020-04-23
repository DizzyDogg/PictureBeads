from base64 import b64decode
from base64 import b64encode
from io import BytesIO

from fastapi import Body
from fastapi import FastAPI
from fastapi.responses import Response
from PIL import Image

import image_ops

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/resize")
async def resize(image: str = Body(..., embed=True),
                 width: int = 40,
                 height: int = 50):
    image = Image.open(BytesIO(b64decode(image)))
    buf = BytesIO()
    image_ops.resize(image, (width, height)).save(buf, format="PNG")
    out_b64 = b64encode(buf.getvalue())
    return {"image": out_b64}


@app.post("/generate_pixelart")
async def generate_pixelart(image: str = Body(..., embed=True),
                            red: float = 1.0,
                            green: float = 1.0,
                            blue: float = 1.0):
    image = Image.open(BytesIO(b64decode(image)))
    buf = BytesIO()
    image_ops.generate_pixelart(
        image, red, green, blue).save(buf, format="PNG")
    out_b64 = b64encode(buf.getvalue())
    return {"image": out_b64}


@app.post("/generate_pattern")
async def generate_pattern(image: str = Body(..., embed=True)):
    return Response()
