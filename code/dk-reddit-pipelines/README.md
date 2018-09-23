## Create the conda environment

```bash
conda update -n base conda
conda env create -f environment.yml
```

## Getting data

- We use the `praw` package
- Documentation links
  - [The Reddit Class](https://praw.readthedocs.io/en/latest/code_overview/reddit_instance.html)
  - [Front Page](https://praw.readthedocs.io/en/latest/code_overview/reddit/front.html)
  - [Subreddit](https://praw.readthedocs.io/en/latest/code_overview/reddit/subreddit.html)
- First, we create an object of class `Reddit()` by passing the `OAuth` credentials
- Create a `Front` or `subreddit` object to extract posts/submissions etc.
- [Reference](http://www.storybench.org/how-to-scrape-reddit-with-python/)
