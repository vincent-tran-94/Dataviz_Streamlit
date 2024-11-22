import streamlit as st

from visualisation import *
from data_preprocessing import *


path_csv_1 = "data/tweets_users_chatgpt.csv"
path_csv_2 = "data/tweets_preprocess.csv"

st.cache_data.clear()

st.set_page_config(
    page_title="Tweets ChatGPT",
    page_icon="𝕏",
    layout="wide"
)

try:
    df = load_data(path_csv_1)
    df2 = load_data(path_csv_2)
except Exception as e:
    st.error(f"Erreur lors du chargement des données: {str(e)}")
    st.stop()

# Application principale
st.title("Analyse des Tweets pour des utilisateurs lors de la sortie de ChatGPT")
st.markdown("**Calcul des métriques** : likes, retweets, tweets, followers, amis et nombre de mots différents")

user_metrics = (
    df2.groupby("User")
    .agg(
        total_likes=("Likes", "sum"),
        total_retweets=("Retweets", "sum"),
        total_tweets=("Tweet", "count"),
        total_followers=("UserFollowers", "max"),
        total_friends=("UserFriends","max"),
        unique_words=("processed_tweet", lambda x: sum(count_unique_words(tweet) for tweet in x)),
    )
    .reset_index()
)

# Filtrer par utilisateur
selected_user = st.selectbox("Choisissez un utilisateur :", user_metrics["User"].unique())
if selected_user:
    user_data = user_metrics[user_metrics["User"] == selected_user].iloc[0]

    st.markdown(f"### Métriques pour l'utilisateur : **{selected_user}**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre de Likes", int(user_data["total_likes"]))
    col2.metric("Nombre de Retweets", int(user_data["total_retweets"]))
    col3.metric("Total de Tweets postés", user_data["total_tweets"])

    col4, col5, col6 = st.columns(3)
    col4.metric("Nombre de Followers", int(user_data["total_followers"]))
    col5.metric("Nombre d'amis", int(user_data["total_friends"]))
    col6.metric("Total de mots uniques", user_data["unique_words"])


# Métriques globales
st.markdown("### Métriques globales :")
all_tweets = df2["processed_tweet"].tolist()
st.metric("Total des utilisateurs", len(user_metrics))

with st.sidebar:
    st.title("Dashboard sur l'Analyse des Tweets sur ChatGPT")
    st.subheader("Introduction")
    st.markdown("""
    Ce dashboard explore l'impact de ChatGPT sur Twitter en analysant environ 300 000 tweets. 
                        À travers cette étude, nous examinons l'enthousiasme des utilisateurs, 
                        les tendances émergentes et l'évolution de l'outil. L'objectif est de mieux comprendre les perceptions publiques, 
                        les facteurs influençant ChatGPT, et ses applications potentielles. Grâce à des analyses sur le volume de tweets, 
                        le sentiment, l'engagement et les événements clés liés à l'IA, ce dashboard fournit des insights précieux pour 
                        guider les stratégies des entreprises, chercheurs et décideurs.
    """
    )
    st.subheader("Selection de pages")


page = st.sidebar.radio("Select a page", ["Description Dataset", "Visualisations"])
# Display selected page
if page == "Description Dataset":
    page1(df,df2)
elif page == "Visualisations":
    tab1, tab2, tab3, tab4, tab5 = page2(df2)

    
