from fastbook import *
import streamlit as st
from os.path import exists

#next bit needed for windows
# import pathlib
# temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath


@st.cache(allow_output_mutation=True)
def loads():
    
    filename = 'IMDB_class_model_export.pkl'
    file_exists = exists(filename)

    # if file doesn't exist load it from GitHub
    if not file_exists:
        with st.spinner("Downloading model... this may take a while! \n Don't stop it!"):

            import urllib

            # file more than 200MB so added as a realease on github
            # url is https://github.com/spacebluebamboo/nlp_sentiment_streamlit/releases/tag/V2
            # so modified slightly and included file name
            url='https://github.com/spacebluebamboo/nlp_sentiment_streamlit/releases/download/V2/IMDB_class_model_export.pkl'
            

            urllib.request.urlretrieve(url, filename)
        return []
    #if it does create the learner
    else:
        learner = load_learner(filename)
        return learner
        

# Load the data
learner=loads()

# Stuff on streamlit
txta = st.text_area('Enter text') 

ll = learner.predict(txta)

scora = 100-int(ll[2][0]*100)
sent = ll[0]
if sent=='pos':
    sent='Positive'
elif sent=='neg':
    sent='Negative'
else:
    sent='??'

st.title("Rating =  {}  / 100".format(scora))
st.title("Overall sentiment is {}".format(sent) )