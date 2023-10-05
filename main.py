from typing import Union
from fastapi import FastAPI
from lib.broadcast import send_notification

app = FastAPI()

@app.get("/")
def read_root():
    send_notification('my-event', {'message': 'Hello World'})
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}