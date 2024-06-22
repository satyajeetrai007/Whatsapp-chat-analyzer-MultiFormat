import re 
import pandas as pd
import datetime

def preprocessing(data):

    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    message = re.split(pattern,data)[1:]

    dates = re.findall(pattern,data)

    df = pd.DataFrame({'messages':message,
                        'dates':dates
                                         })
    
    date_str_cleaned = df['dates'].replace('\u202f', ' ')

    # Defined the correct format string
    date_format='%d/%m/%Y, %H:%M - '

    # Converted to datetime
    date_time_obj = pd.to_datetime(date_str_cleaned, format=date_format)

    df['dates'] = date_time_obj

    df.rename(columns={'dates':'date'},inplace = True)

    # fn to extract users and messages
    users = []
    messages = []
    for message in df['messages']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['message'] = messages
    df.drop(columns=['messages'],inplace = True)

    # extracting useful info from date column
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['min'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month_name'] = df['date'].dt.month_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period


    return df

