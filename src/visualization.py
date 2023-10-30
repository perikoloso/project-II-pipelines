import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


sns.set_context("poster")
sns.set(rc={"figure.figsize": (12.,6.)})
sns.set_style("whitegrid")

def chart_types(df):
    plt.show()
    plt.figure(figsize=(12,4))
    sns.countplot(x="category",data=df)
    plt.xlabel("Categories")
    plt.title("Cocktails by category")
    plt.ylabel('Num of Cocktails')
    plt.show()

    # Return the Seaborn plot (optional)
    return plt


def graph_nutricion(df):
    plt.show()
    plt.figure(figsize=(12,4))
    sns.scatterplot(x="category", y="diff_nutrition",data=df);
    plt.xlabel("Categories")
    plt.title("Cocktails by category")
    plt.ylabel('Num of Cocktails')
    plt.show()

    # Return the Seaborn plot (optional)
    return plt
