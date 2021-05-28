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

# disables the misconfiguration error message.
st.set_option('deprecation.showPyplotGlobalUse', False)
#title of the app
st.title("Amazon Review Dashboard")
#sidebar
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
#reads the uploaded file as a dataframe
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
        #shows a dropdown list 
        select = st.selectbox('Select year', df.year.unique())
        #creating a new dataframe that contains only rows from the select year.
        data = df[df['year']==select]
        

  
    with col2:
        
        #Total review
        yearSelected = data.year.iloc[0]
        st.subheader(' %s Total Reviews' % (yearSelected))
        total = data.month.count()
        st.title(total)

        #total positive review
        st.subheader(' Total Positive Reviews')
        #selecting rows that are positive
        total = data[data.Class== 'positive'].shape[0]
        st.title(total)
        
        #total negative review
        st.subheader(' Total Negative Reviews')
        #selecting rows that are negative
        total = data[data.Class== 'negative'].shape[0]
        st.title(total)
        
        
        
    with col3: 
        #Pie chart Graph : display Sentiment
        sentiment_count = data['Class'].value_counts()#counts the number of classes
         # order the data by sentiment 
        sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Reviews': sentiment_count.values})
        #creates the figure
        fig = px.pie(sentiment_count, names='Sentiment', values='Reviews', hole=.3, width=50)
        #display the chart
        st.plotly_chart(fig, use_container_width=True) 



    with section4: 
        #creating the month graph
        st.header("Month")
        #creating a multiselect search bar
        choice = st.multiselect('Select month',('January','February','March','April','May','June','July','August','September','October','November','December'), key='0')
        
        #setting up a default function when the searchbar is empty
        if len(choice) > 0:
            # creating a new datafram that select only the month columns and check if the choices from the multi-select exist on the dataframe.
            choice_data = data[data.month.isin(choice)]
            fig_choice = px.histogram(choice_data, x='month', y='Class', histfunc='count', color='Class',
            facet_col='Class', labels={'Class':'Reviews'})
            #display the chart
            st.plotly_chart(fig_choice, use_container_width=True)
            
            
    with col4: 
        #review table
        st.header('%s  %s Review Table' % (choice, yearSelected))      
        sentiment = st.radio('Sentiment',('positive','negative'))
        data = data[data.month.isin(choice)]
        data = data[data['Class']== sentiment]
        text = pd.DataFrame(data[['month','Class','reviewText']])
        st.write(text)

        
    with col5: 
         #word cloud 
        #display the selected year
        st.header('%s  %s  Word Frequency' % (choice, yearSelected))
        st.subheader('What are people talking?')
        #display the chosen sentiment
        st.markdown(' Sentiment: %s ' % (sentiment))
        df = data[data['Class']==sentiment]
        words = ' '.join(df['reviewText']) #creates a list of words from the review column
        processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
        #removing special characters  and stopwords
        wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black', width=800, height=800).generate(processed_words)
        #generates the word cloud as image
        plt.imshow(wordcloud)
        # removes sticks by creating an empty list
        plt.xticks([])
        plt.yticks([])
        #display the word cloud
        st.pyplot()


            
                
except Exception as e:
    st.write("Please upload file to the application")


    


        
