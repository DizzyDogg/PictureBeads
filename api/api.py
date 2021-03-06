from base64 import b64decode
from base64 import b64encode
from base64 import urlsafe_b64encode
from email.message import EmailMessage
import imghdr
from io import BytesIO
import os
import pickle

from fastapi import Body
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from googleapiclient.discovery import build
from googleapiclient import errors
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

import image_ops
import settings


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

app = FastAPI()


@app.get("/")
async def root():
    """
    Simple test endpoint
    """

    return {"message": "Hello World!"}


@app.post("/resize")
async def resize(image: str = Body(..., embed=True),
                 width: int = 40,
                 height: int = 50):
    """
    Takes an image, a width, and a height, and returns a copy of the image
    resized to the given size.
    """

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
    """
    Takes a pre-scaled image and returns a copy converted to use a palette
    of available colors. If provided, the red, green, and blue values are
    used to scale the corresponding color channels of the image first.
    """

    image = Image.open(BytesIO(b64decode(image)))
    buf = BytesIO()
    image_ops.generate_pixelart(
        image, red, green, blue).save(buf, format="PNG")
    out_b64 = b64encode(buf.getvalue())
    return {"image": out_b64}


def _generate_pattern(image, flip=True):
    template = image_ops.generate_template(image, flip=flip)
    image_buf = BytesIO()
    template.save(image_buf, format="PNG")
    bead_counts = image_ops.count_beads(image)

    # Start PDF
    data = BytesIO()
    # bottomup is forced because reportlab treats images that way?
    # Or we could flip the image ourselves and still specify the bottom
    # right corner?
    canvas = Canvas(data, bottomup=1, pagesize=letter)

    # page 1: packing list and instructions
    y = 10 * inch
    color_count = len(bead_counts.keys())
    column = 0
    left_margin = 0.5 * inch
    for index, color_name in enumerate(sorted(bead_counts.keys())):
        if column == 0 and index >= color_count / 2.0:
            column = 1
            left_margin = 4.25 * inch
            y = 10 * inch
        count = bead_counts[color_name]
        color_file = color_name.replace(" ", "_") + ".png"
        canvas.drawInlineImage(
            f"data/color_images/bitmap/{color_file}",
            x=left_margin+0.5*inch, y=y-0.04*inch,
            width=0.2*inch, height=0.2*inch
        )
        canvas.drawCentredString(left_margin+0.25*inch, y, str(count))
        canvas.drawString(left_margin+0.75*inch, y, color_name)
        y -= 0.2 * inch
    canvas.showPage()

    # page 2: template
    canvas.drawInlineImage(
        template,
        x=0.25*inch, y=0.5*inch,
        width=8*inch, height=10*inch,
    )
    canvas.showPage()

    # Finalize and return
    canvas.save()
    data.seek(0)
    return data.read()


# TODO: Refactor the PDF generation part of this into its own thing
@app.post("/generate_pattern")
async def generate_pattern(
    image: str = Body(..., embed=True),
    flip: bool = Body(True, embed=True),
):
    """
    Takes an image as output by the `generate_pixelart` call, and returns a
    PDF with the following pages:

        1. Packing list/instructions
        2. Template
    """

    # Process image
    image = Image.open(BytesIO(b64decode(image)))
    data = _generate_pattern(image, flip=flip)
    return StreamingResponse(data, media_type="application/pdf")


@app.post("/submit_order")
async def submit_order(image: str = Body(..., embed=True),
                       name: str = Body(..., embed=True),
                       email: str = Body(..., embed=True),
                       phone: str = Body(..., embed=True),
                       kit: str = Body(..., embed=True),
                       flip: bool = Body(True, embed=True),
                       pegboard: bool = Body(..., embed=True),
                       tweezers: bool = Body(..., embed=True),
                       frame: bool = Body(..., embed=True),
                       total: int = Body(..., embed=True),
                       ):
    message = EmailMessage()
    message["Subject"] = settings.SUBJECT
    message["To"] = settings.TO
    message["From"] = settings.FROM

    info = f"""
    name: {name}
    email: {email}
    phone: {phone}
    kit: {kit}
    pegboard: {pegboard}
    tweezers: {tweezers}
    flipped: {flip}
    frame: {frame}

    TOTAL: {total}
    """
    # Get binary data from "data:" URL
    image = b64decode(image.split(",")[1])
    pattern = _generate_pattern(Image.open(BytesIO(image)), flip=flip)
    message.preamble = info
    message.set_content(info)
    message.add_attachment(
        image, maintype="image", subtype=imghdr.what(None, image))
    message.add_attachment(
        pattern, maintype="application", subtype="pdf")

    try:

        service = build(
            "gmail", "v1", credentials=CREDS, cache_discovery=False)
        gmail_message = (
            service.users()
            .messages()
            .send(
                userId=settings.FROM,
                body={
                    "raw": urlsafe_b64encode(
                        message.as_bytes()
                    ).decode("utf-8")
                })
            .execute())
        print(f"Message id: {gmail_message['id']}")
    except errors.HttpError as error:
        print(f"An error occurred: {error}")


def get_gmail_credentials():
    token_file = "token.pickle"
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            return pickle.load(token)
    else:
        print("Missing token.pickle file")
        return None


CREDS = get_gmail_credentials()
