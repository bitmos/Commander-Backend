from asyncio import tasks
from datetime import datetime, timedelta
import io
import re
from PIL import Image
from apps.TextAnalysis.TextPredict import textAnalysis
from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson.json_util import ObjectId
from apps.TextAnalysis.TextPredict import textAnalysis
from .models import TaskModel, UpdateTaskModel
from apps.pymongoClient.mongoClient import client
from apps.scrapeR.Scrape import scrapeTwitter , CrawlWeb
from fastapi import File,UploadFile
import pandas as pd
from apps.ImageMap.border import predict
from apps.todo.FindCustom import output
router = APIRouter()

@router.post("/predictborder", response_description="Add new task")
async def create_task(request: Request,file: UploadFile = File(...)) -> str:
    img = Image.open(file.file)
    img = img.save("apps/ImageMap/test/new/test.png") 
    response=predict("apps/ImageMap/test/")
    return response


@router.get("/getDailyScrape", response_description="List dailye")
async def list_tasks(request: Request):
    hads = []
    for had in client.sih_db_new.ArticalScraped.find():
        print(had)
        hads.append(had["href"])
    return hads
    # pos= client.sih_db_new.ArticalScraped.find()
    # df = pd.DataFrame(list(pos)).to_dict("records")
    # return df

@router.post("/predicttext", response_description="Predict and Return")
async def create_task(request: Request, text:str = Body(..., embed=True)):
    return textAnalysis(text)

@router.post("/keywordScrape", response_description="Scrape Custom")
async def create_task(request: Request, keyword:str = Body(..., embed=True)):
    last_hour_date_time = datetime.now() - timedelta(hours = 12)
    d=client.sih_db_new.text_scrape.find({"_id":ObjectId('6306e5efdb96fd40a28e1bbf')},{"hashtags"})
    for doc in d:
        hash=doc["hashtags"]
    hash.append(keyword)
    request.app.mongodb["text_scrape"].update_one({"_id":ObjectId('6306e5efdb96fd40a28e1bbf')},{"$set":{"hashtags":hash}})
    scrapeTwitter(keyword,last_hour_date_time.strftime("%Y-%m-%d %H:%M:%S"),1)
    return {"message":"success"}


@router.post("/ArticleScrape", response_description="Scrape Custom Links")
async def create_task(request: Request,linkto:str = Body(..., embed=True)):
    try:
        retvar = CrawlWeb(linkto,1)   
    except Exception as e:
        return {"message":str(e)}
    return {"message":retvar}


@router.get("/getCustomScrape", response_description="List CustomScrape")
async def list_tasks(request: Request):
    # hads = []
    # a=client.sih_db_new.custom_scrape.find().sort({'_id':-1}).limit(1)
    # i=0
    # for had,i in a:
    #     hads.append(had[i])
    had = output()
    return {"message": had }
    # pos=await request.app.mongodb["custom_scrape"].find()
    # return pos

@router.get("/getCustomScrapeTwitter", response_description="List CustomScrape Twitter")
async def list_tasks(request: Request):
    pos=await request.app.mongodb["customTwitter"].find()
    return pos




@router.get("/", response_description="List all tasks")
async def list_tasks(request: Request):

    tasks = []
    pos=await request.app.mongodb["TwitterAnalyzed"].count_documents({"Predicted": "Positive"})
    neg=await request.app.mongodb["TwitterAnalyzed"].count_documents({"Predicted": "Negative"})
    neu=await request.app.mongodb["TwitterAnalyzed"].count_documents({"Predicted": "Neutral"})
    return {"data":[pos,neg,neu]}

@router.get("/no_flagged", response_description="List all tasks")
async def list_tasks(request: Request):
    pos=await request.app.mongodb["TwitterAnalyzed"].count_documents({})
    cyc=client.sih_db_new.mis.find()
    print(type(cyc))
    for doc in cyc:
        cyc=doc['count']
    return {"flagged_number":pos,"Scraped":cyc}

@router.get("/negtweets", response_description="List all tasks")
async def list_tasks(request: Request):
    neg=client.sih_db_new.TwitterAnalyzed.find({"Predicted": "Negative"})
    data={}
    for doc in neg:
        data[doc['username']]={"tweet":doc['tweet'],"nlikes":doc['nlikes'],"nreplies":doc['nreplies'],"Retweets":doc["nretweets"],"Link":doc["conversation_id"]}
    return data