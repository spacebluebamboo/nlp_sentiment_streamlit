from fastbook import *
import streamlit as st
from os.path import exists

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# #next bit needed for windows
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

# @st.cache(allow_output_mutation=True)
def loadCSV():
    df = pd.read_csv('./EldenReview.csv')
    
    scoreALL=[]
    scoreALL2=[]
    
    for ii,dada in enumerate(df.index):
        txta = df.iloc[ii,0] 
#        NN score
        ll = learner.predict(txta)
        scora = 100-int(ll[2][0]*100)
        scoreALL.append(scora)
#        vader score
        scoreALL2.append( SentimentIntensityAnalyzer().polarity_scores(txta)['compound'] )
        
    df.insert(2,'Predict IMDB',scoreALL)
    df.insert(3,'Predict vader',scoreALL2)
    return df
        

# Load the data
learner=loads()

# a selection box load data or one piece
chois=['Single text in box below','A loaded CSV file','An example CSV file']
choiBIG=st.sidebar.radio('Select', chois)

choiBIG

# analyse text in a box
if choiBIG==chois[0]:
    
    txta = st.text_area('Enter text') 

    if st.button('Run'):
       ll = learner.predict(txta)      


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

# a given text file
elif choiBIG==chois[2]:
    
    # a selection box load data or one piece
    chois2=['Data Frame','Word Cloud','Score Pie','Score Histogram','Plot scores']
    choi2BIG=st.sidebar.radio('Select', chois2)
    df = loadCSV()
    if choi2BIG==chois2[0]:#dataframe
        st.dataframe(df)
    elif choi2BIG==chois2[1]:#word cloud
        texta=[]
        for ii,dada in enumerate(df.index):
            texta.append( df.iloc[ii,0]  )
        texta=''.join(texta)
        wordcloud = WordCloud(max_font_size=40,min_word_length=3).generate(texta)
        fig=plt.figure();
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(fig)
        
    elif choi2BIG==chois2[2]:#pie chart
        scoreAll=df['Predict IMDB']

        neu=[ii for ii,aa in enumerate(scoreAll) if aa>33 and aa<67]
        pos = [ii for ii,aa in enumerate(scoreAll) if aa>=67]
        neg = [ii for ii,aa in enumerate(scoreAll) if aa<=33]

        pieParts=[len(pos), len(neu),len(neg)]
        labels = 'Positive', 'Neutral', 'Negative'
        cols='g','b','r'
        explode=(.04,.04,.04)


        fig, ax = plt.subplots()
        ax.pie(pieParts,labels=labels,autopct='%1.0f%%',
                explode=explode, startangle=0,colors=cols);
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('IMDB')
        st.pyplot(fig)
        
        ###############################
        scoreAll=df['Predict vader']
        tp,tn=.33,-.33
        neu=[ii for ii,aa in enumerate(scoreAll) if aa<tp and aa>tn]
        pos = [ii for ii,aa in enumerate(scoreAll) if aa>=tp]
        neg = [ii for ii,aa in enumerate(scoreAll) if aa<=tn]

        pieParts=[len(pos), len(neu),len(neg)]
        labels = 'Positive', 'Neutral', 'Negative'
        cols='g','b','r'
        explode=(.04,.04,.04)


        fig, ax = plt.subplots()
        ax.pie(pieParts,labels=labels,autopct='%1.0f%%',
                explode=explode, startangle=0,colors=cols);
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Vader')
        st.pyplot(fig)
    elif choi2BIG==chois2[3]:
        
        scoreAll=df['Predict IMDB']
        fig,ax=plt.subplots()
        plt.hist(scoreAll);
        plt.xlabel('Score IMDB')
        plt.ylabel('Frequency')
        st.pyplot(fig)
        
        scoreAll=df['Predict vader']
        fig,ax=plt.subplots()
        plt.hist(scoreAll);
        plt.xlabel('Score vader')
        plt.ylabel('Frequency')
        st.pyplot(fig)
        
    elif choi2BIG==chois2[4]:
        scoreAll=df['score']
        scoreAlli=df['Predict IMDB']
        scoreAllv=df['Predict vader']
        scoreAllv=(scoreAllv+1)*50
        
        fig,ax=plt.subplots()
        
        plt.plot(scoreAll, scoreAlli,'ob',markersize=20,fillstyle="top")
        plt.plot(scoreAll, scoreAllv,'pr',markersize=20)
        plt.plot([0, 50, 100], [0, 50, 100],'k--')
        plt.grid()
        ax.legend(['IMDB','vader'])
        plt.xlabel('Score')
        plt.ylabel('Prediction')
        
        st.pyplot(fig)
        
        