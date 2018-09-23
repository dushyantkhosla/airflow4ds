path_home = '/Users/dkhosla/Dropbox/01-git/airflow4ds/code/dk-reddit-pipelines'

import configparser
import praw

cp = configparser.ConfigParser()
cp.read(f'{path_home}/dags/source/config.ini')
configs_ = cp['reddit.com']

# We begin by creating an instance of `Reddit()`
reddit = praw.Reddit(
    client_id=configs_['personal_use_script'],
    client_secret=configs_['secret_key'],
    user_agent=configs_['app_name'],
    username=configs_['meranaam'],
    password=configs_['khuljasimsim']
)

r_jokes = reddit.subreddit('Jokes', )

list_ = [x.title for x in r_jokes.top(limit=10)]
print(list_)
