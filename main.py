from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
# from apps.TextAnalysis.TextPredict import PredictText
from fastapi.middleware.cors import CORSMiddleware
from apps.scrapeR.Scrape import scraperThread
from apps.TextAnalysis.TextPredict import PredictTextThread
from apps.todo.routers import router as todo_router
from apps.scrapeR.Scrape import scrapeArtical
# from apps.HashMap.routers import router as hashmap
import logging
import threading
import time


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient('mongodb://localhost:27017')
    app.mongodb = app.mongodb_client['sih_db_new']


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(todo_router, tags=["tasks"], prefix="/task")
# app.include_router(hashmap, tags=["state"], prefix="/statecount")


# def thread_function():
#     # PredictText("i hate India")
#     print("[-] Repeated timer starting")
#     scraperThread()
#     rt = RepeatedTimer(3600, scraperThread) 
#     PredictTextThread()
#     newRt = RepeatedTimer(3660, PredictTextThread)
#     scrapeArtical()
#     mynewRt = RepeatedTimer(3660, scrapeArtical)


if __name__ == "__main__":
    # format = "%(asctime)s: %(message)s"
    # logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
    # x = threading.Thread(target=thread_function)
    # x.start()
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )