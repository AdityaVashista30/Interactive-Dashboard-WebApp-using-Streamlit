import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

st.title("Sentiment Anlysis of Tweets about US Airlines")
st.sidebar.title("Sentiment Anlysis of Tweets about US Airlines")

st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown("Navigation and Control Pannel")

DATA_URL=("F:\Projects\Guided Project- Interactive Dashboard using streamlit\Tweets.csv")

@st.cache(persist=True,hash_funcs={pd.DataFrame: lambda _: None})
def load_data():
    data=pd.read_csv(DATA_URL)
    data['tweet_created']=pd.to_datetime(data['tweet_created'])
    return data

data=load_data()

st.sidebar.subheader("Show random tweet")

random_tweet=st.sidebar.radio("Sentiment",('Positive','Neutral','Negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet.lower()')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment")
select=st.sidebar.selectbox('Visualization Type',['Bar Chart','Pie Chart'],key='1')
sentiment_count=data['airline_sentiment'].value_counts()
sentiment_count=pd.DataFrame({'Sentiment':sentiment_count.index,'Tweets':sentiment_count.values})

if st.sidebar.checkbox("Show Chart",True):
    st.markdown("### Number of tweets by sentiments")
    if select=="Bar Chart":
        fig=px.bar(sentiment_count,x='Sentiment',y="Tweets",color="Tweets",height=500)
        st.plotly_chart(fig)
    else:
        fig=px.pie(sentiment_count,values='Tweets',names='Sentiment')
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are users tweeting from?")
hour=st.sidebar.slider("Hour of day",0,23)
modified_data=data[data['tweet_created'].dt.hour==hour]
if not st.sidebar.checkbox("Close",True,key='1'):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00"%(len(modified_data),hour,(hour+1)))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data",False,key='2'):
        st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice=st.sidebar.multiselect("Pick Airlines",('US Airways','United','Southwest','Delta','Virgin America'),key='0')

if len(choice)>0:
    choice_data=data[data.airline.isin(choice)]
    fig_choice=px.histogram(choice_data,x='airline',y='airline_sentiment',histfunc='count',color="airline_sentiment",
    facet_col='airline_sentiment',labels={'airline_sentiment':'tweets'},height=600,width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment=st.sidebar.radio("Display word cloud of sentiment:",('Positive','Negative','Neutral'))

if not st.sidebar.checkbox("Close Word Box",True,key='4'):
    st.header('Word cloud for %s sentiment'%(word_sentiment))
    df=data[data['airline_sentiment']==word_sentiment.lower()]
    words=' '.join(df['text'])
    processed_words=' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word !='RT'])
    wordcloud=WordCloud(stopwords=STOPWORDS,background_color='yellow',height=640,width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
