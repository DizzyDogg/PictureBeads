from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/test")
@app.post("/test")
async def echo(foo="", bar=""):
    return {"foo": foo, "bar": bar}
