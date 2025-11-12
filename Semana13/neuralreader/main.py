# main.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import os
from neural_core import entrenar_con_pdf, responder

app = FastAPI(title="NeuralReader Web")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_pdf(file: UploadFile):
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    msg = entrenar_con_pdf(file_path)
    return {"status": msg}

@app.post("/ask/")
async def ask_question(q: str = Form(...)):
    respuesta = responder(q)
    return {"response": respuesta}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
