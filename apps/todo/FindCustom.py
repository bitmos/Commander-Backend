from apps.pymongoClient.mongoClient import client
import pandas as pd 

db = client["sih_db_new"]
keyword = db['custom_scrape']

def output():
    x = keyword.find()
    df =  pd.DataFrame(list(x))
    zero = df.iloc[1]
   
    return zero[1]