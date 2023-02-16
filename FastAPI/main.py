from fastapi import FastAPI
from routers import controllers

import uvicorn

app = FastAPI(title='Okatron AI')
app.include_router(controllers.router)

if __name__ == '__main__':
    # コンソールで [$ uvicorn run:app --reload]でも可
    uvicorn.run(app=app, port=8000)