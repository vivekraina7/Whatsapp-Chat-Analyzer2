import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocessor(data)
    st.dataframe(df)

    #  fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    st.title('Top Statistics')

    if st.sidebar.button('Show Analysis'):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Total Media Messages')
            st.title(num_media_messages)

        with col4:
            st.header('No of links')
            st.title(num_links)

        # monthly timeline
        timeline = helper.monthly_timeline(selected_user,df)
        st.title('Monthly Timeline')
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='lightseagreen')
        ax.grid(linestyle = '--')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots(figsize=(20,5))
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='lightseagreen')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.title('Most Busy Day')
            weekly_activity = helper.weekly_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(weekly_activity.index,weekly_activity.values,color='lightseagreen')
            #ax.bar_label(bars, label_type='center', color='#FDFFF6', fontsize=11)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.title('Most Busy Month')
            monthly_activity = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.plot(monthly_activity.index,monthly_activity.values,color='lightseagreen')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(20,5))
        ax = sns.heatmap(user_heatmap, cmap="BuGn")
        st.pyplot(fig)


        #  Finding the busiest users in the group(Group Level)
        if selected_user == 'Overall':
            st.title('Most Busy users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2, col3 = st.columns(3)

            with col1:
                ax.bar(x.index,x.values,color='lightseagreen')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

            with col3:
                figg, bx = plt.subplots()
                mycolors = ['#1d6353','#218f79','#21b098','#83d4b3','#dedec1']
                bx.pie(x.values,labels=x.index,colors=mycolors)
                plt.legend(bbox_to_anchor=(0.5,0.05), loc="center right", fontsize=10,
           bbox_transform=plt.gcf().transFigure)
                circle = plt.Circle((0, 0), 0.7, color='white')
                p = plt.gcf()
                p.gca().add_artist(circle)
                st.pyplot(figg)

        # Wordcloud
        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        bars = ax.barh(most_common_df[0],most_common_df[1],color='lightseagreen')
        ax.bar_label(bars,label_type='center',color='#FDFFF6', fontsize=7)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.title('Emoji Analysis')
        emoji_df = helper.emoji_helper(selected_user, df)

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head())
            st.pyplot(fig)
    
        import nltk
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        # import nltk
        nltk.download('vader_lexicon')

        sid = SentimentIntensityAnalyzer()

        for_sentiment = 'a person is a person no matter how small dr seuss i teach the smallest students with the biggest enthusiasm \
        for learning my students learn in many different ways using all of our senses and multiple intelligences i use a wide range\
        of techniques to help all my students succeed students in my class come from a variety of different backgrounds which makes\
        for wonderful sharing of experiences and cultures including native americans our school is a caring community of successful \
        learners which can be seen through collaborative student project based learning in and out of the classroom kindergarteners \
        in my class love to work with hands on materials and have many different opportunities to practice a skill before it is\
        mastered having the social skills to work cooperatively with friends is a crucial aspect of the kindergarten curriculum\
        montana is the perfect place to learn about agriculture and nutrition my students love to role play in our pretend kitchen\
        in the early childhood classroom i have had several kids ask me can we try cooking with real food i will take their idea \
        and create common core cooking lessons where we learn important math and writing concepts while cooking delicious healthy \
        food for snack time my students will have a grounded appreciation for the work that went into making the food and knowledge \
        of where the ingredients came from as well as how it is healthy for their bodies this project would expand our learning of \
        nutrition and agricultural cooking recipes by having us peel our own apples to make homemade applesauce make our own bread \
        and mix up healthy plants from our classroom garden in the spring we will also create our own cookbooks to be printed and \
        shared with families students will gain math and literature skills as well as a life long enjoyment for healthy cooking \
        nannan'
        ss = sid.polarity_scores(for_sentiment)

        for k in ss:
            st.title('{0}: {1}, '.format(k, ss[k]), end='')
