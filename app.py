import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import preprocessing
import HIndividual as i
import HOverall as o

st.sidebar.title(':red[WHA]**LYZER**')

st.sidebar.info("Upload here and select correct format.")
uploaded_file12 = st.sidebar.file_uploader("Choose a file" ,key = '12h')

format = st.sidebar.radio(label = 'format' , options = ['24 hour format','12 hour format'])

if uploaded_file12 is not None:
    
    bytes_data = uploaded_file12.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessing.pre_processing(data,format)

    unique_user_list = df['users'].unique().tolist()
    unique_user_list.remove('group_notification')
    unique_user_list.sort()
    unique_user_list.insert(0,'overall')
    user = st.sidebar.selectbox('Show Analysis For :', unique_user_list)

    if st.sidebar.button('Show Analysis'):
        if user == 'overall':
            o.overall(df,user)
        else :
            i.individual(df,user)

