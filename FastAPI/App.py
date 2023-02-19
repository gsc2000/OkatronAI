import os

from fastapi import FastAPI
from routers import controllers
from fastapi.staticfiles import StaticFiles

import uvicorn

app = FastAPI(title='Okatron AI')
app.include_router(controllers.router)
current = str(os.path.dirname(os.path.abspath(__file__)))
app.mount("/", StaticFiles(directory=current + "/web", html=True), name="web")

if __name__ == '__main__':
    # コンソールで [$ uvicorn run:app --reload]でも可
    uvicorn.run(app=app, host="0.0.0.0", port=8000)