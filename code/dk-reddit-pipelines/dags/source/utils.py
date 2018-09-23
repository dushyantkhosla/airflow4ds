import configparser
import praw

import warnings
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
from pandas import DataFrame

def connect_to_reddit(path_home):
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
