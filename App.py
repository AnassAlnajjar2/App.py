import streamlit as st
import preprocessor
import helper
from matplotlib import pyplot as plt


st.sidebar.title("Whats App Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a Chat")
if uploaded_file is not None:
     # To read file as bytes:f
     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode("utf-8")
     df = preprocessor.preprocess(data)


     user_list = df['user'].unique().tolist()

     try:
          user_list.remove('notification')
     except:
          pass

     user_list.sort()
     user_list.insert(0, 'All Users')
     selected_user = st.sidebar.selectbox("Users", user_list)

     if st.sidebar.button("Show Analysis"):

          if selected_user == "All Users":
               st.title("Top Statistics")

          num_messages, words, links = helper.fetch_stats(selected_user, df)
          audios, stickers, images, video = helper.more_stats(selected_user, df)

          st.header(f"Total Messages: {num_messages}")

          st.header(f"Total Words: {words}")

          st.header(f"Audios Shared: {audios}")

          st.header(f"Stickers Shared: {stickers}")

          st.header(f"Images Shared: {images}")

          st.header(f"Videos Shared: {video}")

          st.header(f"Links Shared: {links}")



          emojis_df = helper.most_used_emojes(selected_user, df)

          st.title(f"Most Used Emoijs: {emojis_df['Emoji'][0]} {emojis_df['Emoji'][1]} {emojis_df['Emoji'][2]}")

          fig = helper.plot_monthly_timeline(selected_user, df)
          st.title("Monthly Timeline")
          st.pyplot(fig)

          fig = helper.plot_daily_timeline(selected_user, df)
          st.title("Daily Timeline")
          st.pyplot(fig)

          fig1 = helper.most_busy_days(selected_user, df)
          fig2 = helper.most_busy_months(selected_user, df)
          st.title("Activity Map")
          col1, col2 = st.columns(2)

          with col1:
              st.header("Most Busy Days")
              st.pyplot(fig1)
          with col2:
              st.header("Most Busy Months")
              st.pyplot(fig2)

          if selected_user == "All Users":
               st.title("Overall Hours")
               fig1, fig2 = helper.am_pm(selected_user, df)
               col1, col2 = st.columns(2)

               with col1:
                   st.header("AM")
                   st.pyplot(fig1)
               with col2:
                   st.header("PM")
                   st.pyplot(fig2)

          if selected_user == 'All Users' and len(df.user.unique()) > 2:
               st.title("Most Active Users in the Group")
               x, new_df = helper.most_active_users(df)
               fig, ax = plt.subplots()

               col1, col2 = st.columns(2)

               with col1:
                    ax.bar(x.index, x.values, color='green')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

               with col2:
                    st.dataframe(new_df)

          st.title("Word Cloud")
          df_wc = helper.create_word_cloud(selected_user, df)
          fig, ax = plt.subplots()
          ax.imshow(df_wc)
          plt.xticks([])
          plt.yticks([])
          st.pyplot(fig)


          most_common_words = helper.most_commen_words(selected_user, df)
          st.title("Most Common Words")

          fig, ax = plt.subplots()
          ax.bar(most_common_words['Word'], most_common_words['Count'], color='red')
          plt.xticks(rotation='vertical')


          st.pyplot(fig)

          st.title("All Emojis Used")
          st.dataframe(emojis_df)
