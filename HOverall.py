import streamlit as st
import matplotlib.pyplot as plt
import re
import pandas as pd
from wordcloud import WordCloud
import emoji
from urlextract import URLExtract
import numpy as np
from collections import Counter
import seaborn as sns

def overall(df,user):
    otop_statistics(df)
    omost_active_users(df)
    omonthly_timeline(df)
    odaily_timeline(df)
    oweekly_Activity_map(df)
    odaily_activity_heatmap(df)
    oword_cloud(df,user)
    omost_common_words(df)
    oemoji_analysis(df)
def otop_statistics(df):


    
    num = df.shape[0]
    df_new = df['users'] !='group_notification'
    df = df[df_new]
    TotalMessages = df['message'].shape[0]
    Group_Messages = num - TotalMessages
    TotalWords = 0
    for message in df['message']:
        TotalWords = TotalWords + np.array(message.split(' ')).shape[0]

    MediaShared = 0
    for message in df['message']:
        if message == '<Media omitted>\n':
            MediaShared = MediaShared + 1

    url_pattern = re.compile(r'(https?://[^\s]+)')
    links = []
    for message in df['message']:
        if url_pattern.findall(message) != []:
            links.append(url_pattern.findall(message))
    NumberOfLinks = len(links)

    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header('Total Messssages')
        st.title(TotalMessages)

    with col2 :
        st.header('Group Notifications')
        st.title(Group_Messages)

    with col3:
        st.header('Total Words')
        st.title(TotalWords)
    
    with col4:
        st.header('Media Shared')
        st.title(MediaShared)

    with col5:
        st.header('Links Shared')
        st.title(NumberOfLinks)
    






def omonthly_timeline(df):

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    st.title('Monthly Timeline')
    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

def odaily_timeline(df):
    timeline = df.groupby(['only_date']).count()['message'].reset_index()

    st.title('Daily Timeline')
    fig,ax = plt.subplots()
    ax.plot(timeline['only_date'], timeline['message'],color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

def odaily_activity_heatmap(df):
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)
def oweekly_Activity_map(df):
    st.title("Weekly Activity")
    busy_day = df['day_name'].value_counts()
    busy_month = df['month_name'].value_counts()

    col1 , col2 = st.columns(2)
    with col1:
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        st.pyplot(fig)
    
    with col2:
        fig,ax = plt.subplots()
        ax.bar(busy_month.index,busy_month.values,color = 'orange')
        plt.xticks(rotation = 90)
        st.pyplot(fig)
    
def omost_active_users(df):
    st.header('Most Active Users')
    Most_busy_user_df = df.groupby('users').count()['message'].reset_index().sort_values(by = 'message',ascending=False)[:10]
    Most_busy_users = Most_busy_user_df['users']
    Most_busy_users_Messages_count = Most_busy_user_df['message']
    Most_busy_users_Messages_percentage = (Most_busy_user_df['message']/df.shape[0])*100
    new_df = pd.DataFrame({'Users':Most_busy_users ,'MessagePercentage':Most_busy_users_Messages_percentage})
    new_df.index = [np.linspace(1,new_df.shape[0],new_df.shape[0])]  
    fig,ax = plt.subplots()
    col1,col2 = st.columns(2)
    with col1:
        ax.bar(Most_busy_users,Most_busy_users_Messages_count)
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
    with col2:
        st.dataframe(new_df)    
def oword_cloud(df,user):
    f = open('.venv\stop_hinglish.txt','r',encoding='utf-8')
    stop_words = f.read().split()

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    

    st.title('WordCloud')
    wc = WordCloud(height=500, width= 500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep = ' '))
    fig,axis = plt.subplots()
    axis.imshow(df_wc)
    st.pyplot(fig)


def omost_common_words(df):
    f = open('.venv\stop_hinglish.txt','r',encoding='utf-8')
    stop_words = f.read().split()



    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20),columns=['Word','frequency'])

    # st.title('Most Common Words Table')
    # st.dataframe(most_common_df)
    st.title('Most Common Word Plot')
    fig,ax = plt.subplots()
    ax.barh(most_common_df['Word'],most_common_df['frequency'])
    plt.xticks(rotation = 90)
    st.pyplot(fig)
    


    
def oemoji_analysis(df):
    emojis = []

    # Access the dictionary of emojis
    emoji_dict = emoji.EMOJI_DATA

    # Extract emojis from messages
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji_dict])

    # Count frequency of each emoji
    emoji_dict = Counter(emojis).most_common()
    emoji_df = pd.DataFrame(emoji_dict,columns = ['Emoji','Frequency'])
    
        

    st.dataframe(emoji_df)
