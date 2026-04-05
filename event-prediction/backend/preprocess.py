# preprocess.py
import pandas as pd

# ---------- DATASET 1 ----------
def load_twitter_dataset(path):
    df = pd.read_csv(path)

    df = df[["Username", "Timestamp", "Retweets"]].copy()

    df.rename(columns={
        "Username": "user_id",
        "Timestamp": "timestamp",
        "Retweets": "retweets"
    }, inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df = df.dropna()

    df["event_id"] = df.index // 50

    return df


# ---------- DATASET 2 ----------
def load_tweets_dataset(path):
    df = pd.read_csv(path)

    df = df[["author", "date_time", "number_of_shares"]].copy()

    df.rename(columns={
        "author": "user_id",
        "date_time": "timestamp",
        "number_of_shares": "retweets"
    }, inplace=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df = df.dropna()

    df["event_id"] = df.index // 50

    return df


# ---------- FEATURE ENGINEERING ----------
def extract_features(event_df):
    tweet_count = len(event_df)
    unique_users = event_df["user_id"].nunique()
    retweet_sum = event_df["retweets"].sum()

    time_span = (event_df["timestamp"].max() - event_df["timestamp"].min()).total_seconds()

    avg_retweets = retweet_sum / tweet_count if tweet_count > 0 else 0
    user_ratio = unique_users / tweet_count if tweet_count > 0 else 0

    return [
        tweet_count,
        unique_users,
        retweet_sum,
        time_span,
        avg_retweets,
        user_ratio
    ]