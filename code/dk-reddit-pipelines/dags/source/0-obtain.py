import os
import sqlite3

import configparser
import praw

import warnings
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

path_home_ = '/Users/dkhosla/Dropbox/01-git/airflow4ds/code/dk-reddit-pipelines'
path_to_db_ = f"{path_home_}/data/reddit.db"

def connect_to_reddit(path_home: str):
    """
    """
    # Get the connection parameters
    cp = configparser.ConfigParser()
    cp.read(f'{path_home}/dags/source/config.ini')
    configs_ = cp['reddit.com']

    # Connect to Reddit
    reddit = praw.Reddit(
        client_id=configs_['personal_use_script'],
        client_secret=configs_['secret_key'],
        user_agent=configs_['app_name'],
        username=configs_['meranaam'],
        password=configs_['khuljasimsim']
    )

    return reddit

def get_post_details(post) -> dict:
    """Parse a given post and return essential info in a Dict
    """
    dict_ = {
        'name_author': post.author.name,
        'timestamp_created': post.created,
        'is_OC': post.is_original_content,
        'num_upvotes': post.ups,
        'num_downvotes': post.downs,
        'num_comments': post.num_comments,
        'is_gilded': post.gilded,
        'post_title': post.title,
        'post_url': post.url,
        'post_text': post.selftext
    }

    return dict_

def scrub_df(df: DataFrame) -> DataFrame:
    """Prepare DataFrame for loading into Sqlite db
    """
    df.loc[:, 'timestamp_created'] = pd.to_datetime(df['timestamp_created'], unit='s')
    df.loc[:, 'is_OC'] = df['is_OC'].astype(int)

    for col in df.select_dtypes(include=np.number).columns:
        df.loc[:, col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')

    df = df.loc[:, ['post_title', 'post_url', 'post_text', 'name_author',
                    'is_OC', 'is_gilded', 'num_comments', 'num_downvotes', 'num_upvotes']]
    return df

def get_topN_posts_TF(subreddit_: str, path_home: str, N: int, TF: str) -> DataFrame:
    """
    Get the Top N posts from any Subreddit for any Time Frame

    Example
    -------
    df_news = get_topN_posts_TF(subreddit_='news',
                                path_home=path_home_,
                                N=20,
                                TF='week')
    """
    # Connect to the subreddit
    reddit = connect_to_reddit(path_home=path_home_)
    r_subr = reddit.subreddit(subreddit_)

    # Get the top N posts of the TF
    genr_posts = r_subr.top(time_filter=TF, limit=N)

    # Parse the posts in to a DataFrame. Clean it up.
    df_posts = DataFrame([get_post_details(x) for x in genr_posts]).pipe(scrub_df)

    return df_posts

def load_posts_to_db(path_to_db: str, df: DataFrame, table_name: str):
    """
    """
    # Connect to target db
    conn_ = sqlite3.connect(path_to_db)
    curs_ = conn_.cursor()

    # Load posts into db
    df.to_sql(
        name=table_name,
        con=conn_,
        if_exists='append',
        index=False
    )
