import matplotlib.pyplot as plt

def class_imbalance(y):
    """
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    y.value_counts(normalize=True).plot.barh(ax=ax)

    ax.set_title("There is no class imbalance\n")
    ax.set_xlabel("\n% of cases")
    ax.set_ylabel("Class\n")

    path_ = "figures/01-class-imbalance.png"
    plt.savefig(path_, bbox_inches='tight')
    print("Plot saved at {}".format(path_))
    return None



def variance_by_group(df, y):
    """
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby(y).mean().T.plot.barh(ax=ax)

    ax.set_title("""Very litte variation across groups in Sepal Width, \nbut Petal Length might be an important predictor \n""")
    ax.set_xlabel("\n Mean Values")
    ax.set_ylabel("Features \n")
    
    path_ = "figures/02-across-groups-variation.png"
    plt.savefig(path_, bbox_inches='tight')
    print("Plot saved at {}".format(path_))
    return None

def anova_results(df):
    """
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    df.plot.barh(ax=ax)

    ax.set_title("ANOVA Results: All predictors are significant \n Petal Length and width are most important \n")
    ax.set_xlabel("\n Score")
    ax.set_ylabel("Predictor \n")

    path_ = "figures/03-ANOVA-results.png"
    plt.savefig(path_, bbox_inches='tight')
    print("Plot saved at {}".format(path_))
    return None
    
    
