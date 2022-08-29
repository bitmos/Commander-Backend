from ast import keyword
from googlesearch import search
from apps.pymongoClient.mongoClient import client
import pandas as pd
import calendar
import time
from datetime import datetime, timedelta
import twint
from apps.TextAnalysis.TextPredict import textAnalysis, PredictTextThread
from duckduckgo_search import ddg

db = client["sih_db_new"]
keyword = db['text_scrape']
article = db['ArticalScraped']
ts = db["twitterScraped"]
cs = db['custom_scrape']


def scrapeArtical():
    CrawlWeb("",0)

def CrawlWeb(urls,choice):
    data = []
    x = keyword.find()
    df =  pd.DataFrame(list(x))
    if choice == 1:
        for i in df['hashtags'][0]:
            print("[+] Searching for: "+i)
            query = f"site:${urls} ${i}"
            for j in search(query, stop=10, pause=10):
                data.append(j)
        final = {str(calendar.timegm(time.gmtime())): data}
        cs.insert_one(final)
        return { "message":"Scrape Done"}
    else:
        for i in df['hashtags'][0]:
            results = ddg(i, region='wt-wt', safesearch='Moderate', time='y', max_results=28)

            article.insert_many(results)

    print('[-] Stored DATA')

def scraperThread():
    print("[-] Starting thread..")
    last_hour_date_time = datetime.now() - timedelta(hours = 2)
    print(last_hour_date_time.strftime("%Y-%m-%d %H:%M:%S"))

    x = keyword.find()
    df =  pd.DataFrame(list(x))
    
    for word in df['hashtags'][0]:
        scrapeTwitter(word, last_hour_date_time.strftime("%Y-%m-%d %H:%M:%S"),0)

def scrapeTwitter(keywords,since,choice):
    print("[-] Scraping Twitter for keywords:", keywords,"Since:",since)
    c = twint.Config()
    c.Search = keywords
    c.Since = since
    c.Pandas = True
    c.Hide_output = True
    c.Count = True
    c.Stats = True
    c.Limit = 150
    twint.run.Search(c)
    tweets = twint.storage.panda.Tweets_df
    data_dict = tweets.to_dict("records")

    try:
        if choice == 1:
            for ind in tweets.index:
                predictions = textAnalysis(tweets['tweet'][ind])
                if predictions == 'class_1':
                    # print("[-] Negative Tweet")
                    negData = tweets.iloc[[ind],]    
                    data_dict = pd.DataFrame(negData)
                    data_dict['Predicted'] = 'Negative' 
                    coldata['mytime'] = time.time()
                    coldata = data_dict.to_dict("records")
                    client.sih_db_new.customTwitter.insert_one(coldata)
                    return { "message":"Scrape Done"}
                else:
                    try:
                        ts.insert_many(data_dict)
                        print("[-] Stored Twitter DATA for the past Hour")
                    except Exception as e:
                        print("[-] Didnt find data :" , e)
    except Exception as e:
        print("[-] Error :",e)



    
    