from urlextract import URLExtract
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import emoji
import streamlit as st
from matplotlib import pyplot as plt


extractor = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'All Users':
        st.title(selected_user, anchor='center')
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df.message:
        words.extend(message.split())

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    val = '\u200eaudio omitted\n'
    audio_value = df[df['message'] == val].shape[0]

    return num_messages, len(words), len(links)

def more_stats(selected_user, df):
    if selected_user != "All Users":
        df=df[df['user'] == selected_user]
    audio_sum = 0
    sticker_sum = 0
    image_sum = 0
    video_sum = 0

    dictt = dict(df['message'].value_counts())

    for p, val in dictt.items():
        if 'audio' in p:
            audio_sum += val

    for p, val in dictt.items():
        if 'sticker' in p:
            sticker_sum += val

    for p, val in dictt.items():
        if 'image' in p:
            image_sum += val

    for p, val in dictt.items():
        if 'video' in p:
            video_sum += val

    return audio_sum, sticker_sum, image_sum, video_sum


def most_active_users(df):
        x = df['user'].value_counts().head()
        new_df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index' : 'name', 'user' : 'precent'})
        return x, new_df



def create_word_cloud(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    temp_df = df[df['user'] != 'notification']
    clean_words = []
    arabic_stopwords = stopwords.words('arabic')
    english_stopwords = stopwords.words('english')

    def remove_strop_words(message):
        clean_words = []
        for word in message.lower().split():
            if word not in english_stopwords and word not in arabic_stopwords:
                if word != 'omitted' and word != '\u200eimage' and word != '\u200esticker' and word != '\u200eaudio' and word != '\u200evideo' and word != '\u200e':
                    clean_words.append(word)
        return " ".join(clean_words)

    temp_df['message'] = temp_df['message'].apply(remove_strop_words)
    text = temp_df['message'].str.cat(sep=" ")
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(text)
    return df_wc


def most_commen_words(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    temp_df = df[df['user'] != 'notification']
    clean_words = []
    arabic_stopwords = stopwords.words('arabic')
    english_stopwords = stopwords.words('english')
    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in arabic_stopwords and word not in english_stopwords:
                if word != 'omitted' and word != '\u200eimage' and word != '\u200esticker' and word != '\u200eaudio' and word != '\u200evideo' and word != '\u200e':
                    clean_words.append(word)

    temp = pd.DataFrame(Counter(clean_words).most_common(20), columns=['Word', 'Count'])
    return temp

def most_used_emojes(selected_user, df):
    if selected_user != "All Users":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(emojis)), columns=['Emoji', 'Count'])
    return emoji_df


def plot_monthly_timeline(selected_user, df):
    if selected_user != "All Users":
        df = df[df['user'] == selected_user]
    df['month_num'] = df['message_date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'], color='green')
    plt.xticks(rotation = 'vertical')
    return fig

def plot_daily_timeline(selected_user, df):
    if selected_user != "All Users":
        df=df[df['user'] == selected_user]
    df['date'] = df['message_date'].dt.date
    daily_timeline = df.groupby('date').count()['message'].reset_index()
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['date'], daily_timeline['message'], color='red')
    plt.xticks(rotation = 'vertical')
    return fig

def most_busy_days(selected_user, df):
    if selected_user != "All Users":
        df=df[df['user'] == selected_user]
    df['day_name'] = df['message_date'].dt.day_name()
    fig, ax = plt.subplots()
    ax.bar(df['day_name'].value_counts().index, df['day_name'].value_counts().values, color='orange')
    plt.xticks(rotation = 'vertical')
    return fig

def most_busy_months(selected_user, df):
    if selected_user != "All Users":
        df=df[df['user'] == selected_user]
    df['month_name'] = df['message_date'].dt.month_name()
    fig, ax = plt.subplots()
    ax.bar(df['month_name'].value_counts().index, df['month_name'].value_counts().values, color='black')
    plt.xticks(rotation = 'vertical')
    return fig

def am_pm(selected_user, df):
    if selected_user != "All Users":
        df=df[df['user'] == selected_user]
    most_hours = df.groupby('hours').count()['message'].reset_index()
    most_hours.replace(to_replace=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                       value=['0AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM'],
                       inplace=True)
    most_hours.replace(to_replace=[12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                       value=['12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM'],
                       inplace=True)
    am = most_hours.iloc[0:12]
    pm = most_hours.iloc[12:24]
    fig1, ax1 = plt.subplots()
    ax1.bar(am['hours'], am['message'], color='orange')
    plt.xticks(rotation='vertical')
    fig2, ax2 = plt.subplots()
    ax2.bar(pm['hours'], pm['message'], color='#50AAB0')
    plt.xticks(rotation='vertical')
    return fig1, fig2