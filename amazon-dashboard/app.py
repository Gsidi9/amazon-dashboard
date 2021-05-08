"""
Author : Goundo  Sidibe
Source : https://jmcauley.ucsd.edu/data/amazon/
Reference: https://www.coursera.org/projects/interactive-dashboards-streamlit-python?action=enroll

INTRODUCTION

In this project, I'm creating a dashboard that would analyse reviews and present meaningful insight on how the customer feels about a product to an Amazon seller. The dashboard would allow Amazon sellers to spot patterns that you may have otherwise missed by staring at a plain old spreadsheet.

"""



#libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.set_option('deprecation.showPyplotGlobalUse', False)
#title of the app
st.title("Amazon Review Dashboard")
st.sidebar.subheader('Sentiment Analysis for Amazon reviews')
st.sidebar.markdown('This application is a dashboard to analyse the sentiment of Amazon reviews')

#setup file upload in sidebar
global df
@st.cache(suppress_st_warning=True)
def load_data(file):
    df = pd.read_csv(file, encoding='utf-8', nrows=50)
    df.columns = ['url', 'redir']
    return df

uploaded_file = st.sidebar.file_uploader("", type="csv", key='file_uploader')

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
                # Mapping the ratings
        df['Class'] = np.where(df.overall > 3,1,0)
        df= df[df.reviewText != 3]
        df.loc[df['Class'] == 0, 'Class'] = 'negative'
        df.loc[df['Class'] == 1, 'Class'] = 'positive'
        df['month'] = pd.to_datetime(df["reviewTime"]).dt.strftime('%B')
        df['year'] = pd.to_datetime(df["reviewTime"]).dt.strftime('%Y')
    except Exception as e:
        df = pd.read_excel(uploaded_file)
        
#containers and columns        
try:       
    section1 = st.beta_container()
    col2,col3= st.beta_columns(2)
    section4 = st.beta_container()
    col4, col5= st.beta_columns(2)
    features = st.beta_container()
    
    
    with section1:
        #setting up the year year
        st.header("Year")
        year = df.year.unique()
        select = st.selectbox('Select year', df.year.unique())
        data = df[df['year']==select]
        

  
    with col2:
        
        #Total review
        yearSelected = data.year.iloc[0]
        st.subheader(' %s Total Reviews' % (yearSelected))
        total = data.month.count()
        st.title(total)

        #Total positive review
        st.subheader(' Total Positive Reviews')
        total = data[data.Class== 'positive'].shape[0]
        st.title(total)
        
        #Total negative review
        st.subheader(' Total Negative Reviews')
        total = data[data.Class== 'negative'].shape[0]
        st.title(total)
        
        
        
    with col3: 
        #Pie chart Graph : display Sentiment
        sentiment_count = data['Class'].value_counts()
        sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Reviews': sentiment_count.values})
        fig = px.pie(sentiment_count, names='Sentiment', values='Reviews', hole=.3, width=50)
        st.plotly_chart(fig, use_container_width=True) 



    with section4: 
        #creating the month graph
        st.header("Month")
        #creating a multiselect search bar
        choice = st.multiselect('Select month',('January','February','March','April','May','June','July','August','September','October','November','December'), key='0')
        
        #setting up a default function when the searchbar is empty
        if len(choice) > 0:
            choice_data = data[data.month.isin(choice)]
            fig_choice = px.histogram(choice_data, x='month', y='Class', histfunc='count', color='Class',
            facet_col='Class', labels={'Class':'Reviews'})
            st.plotly_chart(fig_choice, use_container_width=True)
            
            
    with col4: 
        #Review table
        st.header('%s  %s Review Table' % (choice, yearSelected))      
        sentiment = st.radio('Sentiment',('positive','negative'))
        data = data[data.month.isin(choice)]
        data = data[data['Class']== sentiment]
        text = pd.DataFrame(data[['month','Class','reviewText']])
        st.write(text)

        
    with col5: 
        st.header('%s  %s  Word Frequency' % (choice, yearSelected))
        st.subheader('What are people talking?')
        st.markdown(' Sentiment: %s ' % (sentiment))
        df = data[data['Class']==sentiment]
        words = ' '.join(df['reviewText'])
        processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
        wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black', width=800, height=800).generate(processed_words)
        plt.imshow(wordcloud)
        plt.xticks([])
        plt.yticks([])
        st.pyplot()


            
                
except Exception as e:
    st.write("Please upload file to the application")


    


        