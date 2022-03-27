from fastbook import *
import streamlit as st
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


@st.cache(allow_output_mutation=True)
def loads():
    import gdown

    url = 'https://drive.google.com/uc?id=1F3Qi5s4FJiRGC5hBrAoOpKBLJ9HzvAft'
    output = 'IMDB_class_model_export2.pkl'
    gdown.download(url, output, quiet=False)
    learner = load_learner('IMDB_class_model_export.pkl')
    return learner

learner = loads()
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