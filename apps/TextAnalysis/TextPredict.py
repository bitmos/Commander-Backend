import pandas as pd
from apps.pymongoClient.mongoClient import client
import nltk
from nltk.corpus import stopwords
from keras_preprocessing.sequence import pad_sequences
import keras
import pickle



stemmer = nltk.SnowballStemmer("english")
nltk.download('stopwords')
stopword=set(stopwords.words('english'))

load_model=keras.models.load_model("models/hate&abusive_model.h5")
with open('models/tokenizer.pickle', 'rb') as handle:
    load_tokenizer = pickle.load(handle)

def PredictTextThread():
    print("[-] Starting Predictions..")
    db = client["sih_db_new"]
    # Collection Name
    col = db["twitterScraped"]
    mycol = db['TwitterAnalyzed']
    data = col.find()
    df =  pd.DataFrame(list(data))
    if (df.empty):
        print("No Data")
        return
    
    for ind in df.index:
        predictions = textAnalysis(df['tweet'][ind])
        if predictions == 'class_1':
            negData = df.iloc[[ind],]    
            data_dict = pd.DataFrame(negData)
            data_dict['Predicted'] = 'Negative' 
            coldata = data_dict.to_dict("records")
            spmething = mycol.insert_many(coldata)
            col.delete_one({"username": df['username'][ind]})
        elif predictions == 'class_2':
            posData = df.iloc[[ind],]
            data_dict = pd.DataFrame(posData)
            data_dict['Predicted'] = 'Positive' 
            coldata = data_dict.to_dict("records")
            spmething = mycol.insert_many(coldata)
            col.delete_one({"username": df['username'][ind]})
    return "Done"



def clean(text):
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text

def textAnalysis(text):
    clean(text)
    text=[clean(text)]
    seq = load_tokenizer.texts_to_sequences(text)
    padded = pad_sequences(seq, maxlen=300)
    pred = load_model.predict(padded)
    if pred<0.5:
        return "class_2"
    else:
        return "class_1"