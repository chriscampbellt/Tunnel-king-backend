import asyncio

from fastapi import FastAPI, WebSocket

import ollama


def print_logs(res):
    try:
        if res.total and res.completed:
            percentage = res.completed / res.total * 100
            log_message = f"{res.status} {percentage:.2f}%"
        else:
            log_message = f"{res.status}"
        return log_message
    except Exception as e:
        raise TypeError(f"Error processing response: {res}") from e


async def download_model(model_name: str, websocket):
    for res in ollama.Client().pull(model_name, stream=True):
        log = print_logs(res)
        print("Logging", log)
        await websocket.send_text(f"log {log}")
        await asyncio.sleep(0.01)


async def count(m):
    for i in range(10):
        await asyncio.sleep(2)
        yield i


app = FastAPI()


@app.websocket("/ws/download-model")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        model_name = await websocket.receive_text()
        print("model_name", model_name)
        await download_model(model_name, websocket)
        await websocket.send_text("Download complete.")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()


@app.get("/ping/")
async def read_root():
    return {"ping": "pong"}


# list ollama downloaded models
@app.get("/list-models/")
async def list_models():
    return ollama.Client(
        host="",
    ).list()
