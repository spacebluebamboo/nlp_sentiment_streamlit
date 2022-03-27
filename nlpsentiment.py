from fastbook import *
import streamlit as st
import pathlib
import gdown

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


@st.cache(allow_output_mutation=True)
def loads():
    
    save_dest = Path('model')
    save_dest.mkdir(exist_ok=True)
    
    f_checkpoint = Path("model/IMDB_class_model_export.pkl")

    if not f_checkpoint.exists():
        with st.spinner("Downloading model... this may take a while! \n Don't stop it!"):

            import urllib 


            url='https://github.com/spacebluebamboo/nlp_sentiment_streamlit/releases/download/V2/IMDB_class_model_export.pkl'
            filename =  url.split('/')[-1]

            urllib.request.urlretrieve(url, f_checkpoint)
#             url = 'https://drive.google.com/uc?id=1F3Qi5s4FJiRGC5hBrAoOpKBLJ9HzvAft'
# #             output = f_checkpoint#'IMDB_class_model_export.pkl'
# #             gdown.download(url, output, quiet=False)
#             from GD_download import download_file_from_google_drive
#             download_file_from_google_drive(url, f_checkpoint)
        learner = load_learner(f_checkpoint, map_location=device)
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