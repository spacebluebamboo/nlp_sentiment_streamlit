from fastbook import *
import streamlit as st

import os.path import exists
# import gdown

#next bit needed for windows
# import pathlib
# temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath


@st.cache(allow_output_mutation=True)
def loads():
    
    filename = 'IMDB_class_model_export.pkl'
    file_exists = exists(filename)

    if not file_exists:
        with st.spinner("Downloading model... this may take a while! \n Don't stop it!"):

            import urllib


            url='https://github.com/spacebluebamboo/nlp_sentiment_streamlit/releases/download/V2/IMDB_class_model_export.pkl'
            

            urllib.request.urlretrieve(url, filename)


loads()

filename = 'IMDB_class_model_export.pkl'
file_exists = exists(filename)
file_exists

# txta = st.text_area('Enter text') 

# ll = learner.predict(txta)

# scora = 100-int(ll[2][0]*100)
# sent = ll[0]
# if sent=='pos':
#     sent='Positive'
# elif sent=='neg':
#     sent='Negative'
# else:
#     sent='??'

# st.title("Rating =  {}  / 100".format(scora))
# st.title("Overall sentiment is {}".format(sent) )