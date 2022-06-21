import re
import pandas as pd


def preprocess(data):
    message_pattern = '\[\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{1,2}:\d{1,2}\s\w{2}\]'
    message = re.split(message_pattern, data)[1:]

    date_pattern = '\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{1,2}:\d{1,2}\s\w{2}'
    dates = re.findall(date_pattern, data)

    df = pd.DataFrame({'user_message': message, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M:%S %p')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop('user_message', axis=1, inplace=True)

    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hours'] = df['message_date'].dt.hour
    df['minutes'] = df['message_date'].dt.minute
    df['seconds'] = df['message_date'].dt.second

    return df
