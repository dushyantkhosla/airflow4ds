from sklearn.feature_selection import SelectKBest, f_classif
import pandas as pd

def anova(X, y):
    """
    """
    skb = SelectKBest(k='all', score_func=f_classif)
    skb.fit(X, y)

    return pd.DataFrame({
        'F-score': skb.scores_,
        'P-value': skb.pvalues_}, index=df.columns[:4]
    )