import os
import json
import pandas as pd
from datetime import datetime
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

def break_combined_weeks(combined_weeks):
    """
    Breaks combined weeks into separate weeks.
    
    Args:
        combined_weeks: list of tuples of weeks to combine
        
    Returns:
        tuple of lists of weeks to be treated as plus one and minus one
    """
    plus_one_week = []
    minus_one_week = []

    for week in combined_weeks:
        if week[0] < week[1]:
            plus_one_week.append(week[0])
            minus_one_week.append(week[1])
        else:
            minus_one_week.append(week[0])
            plus_one_week.append(week[1])

    return plus_one_week, minus_one_week

def get_news_df_info(df):
    """
    Extracts various statistics from the news DataFrame.
    
    Args:
        df: pandas DataFrame containing news articles
        
    Returns:
        Tuple with dictionaries of article count by source, word count, etc.
    """
    # Count articles by source
    articles_count_dict = df['source_name'].value_counts().to_dict()
    
    # Count mentions by source
    mentions_count_dict = df['mentions'].dropna().apply(lambda x: len(x.split(','))).groupby(df['source_name']).sum().to_dict()

    # Count links by source
    links_count_dict = df.groupby("source_name")['link_count'].sum().to_dict()
    
    return articles_count_dict, mentions_count_dict, links_count_dict

def get_articles_dict(articles):
    """
    Converts articles data into a dictionary format.
    
    Args:
        articles: list of article dictionaries
        
    Returns:
        Dictionary with article data
    """
    article_list = {
        "article_id": [],
        "title": [],
        "description": [],
        "content": [],
        "source_name": [],
        "published_at": [],
        "category": [],
        "links": [],
        "link_count": []
    }

    for article in articles:
        try:
            article_list["article_id"].append(article.get("article_id", None))
            article_list["title"].append(article.get("title", ""))
            article_list["description"].append(article.get("description", ""))
            article_list["content"].append(article.get("content", ""))
            article_list["source_name"].append(article.get("source_name", ""))
            article_list["published_at"].append(article.get("published_at", ""))
            article_list["category"].append(article.get("category", ""))
            article_list["links"].append(article.get("links", ""))
            article_list["link_count"].append(len(article.get("links", [])))
        except Exception as e:
            print(f"Error processing article: {e}")
    
    return article_list

def convert_2_timestamp(column, data):
    """
    Converts Unix timestamps to readable timestamps.
    
    Args:
        column: column name to be converted
        data: DataFrame with the column
    
    Returns:
        List of formatted timestamps
    """
    if column in data.columns.values:
        timestamp_ = []
        for time_unix in data[column]:
            if pd.isna(time_unix) or time_unix == 0:
                timestamp_.append(None)
            else:
                a = datetime.fromtimestamp(float(time_unix))
                timestamp_.append(a.strftime('%Y-%m-%d %H:%M:%S'))
        return timestamp_
    else:
        print(f"{column} not in data")
        return []

def plot_article_counts(df, top_n=10):
    """
    Plots the top N sources by the number of articles.
    
    Args:
        df: DataFrame with article data
        top_n: Number of top sources to plot
        
    Returns:
        None
    """
    article_counts = df['source_name'].value_counts().head(top_n)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=article_counts.values, y=article_counts.index, palette='viridis')
    plt.xlabel('Number of Articles')
    plt.ylabel('Source Name')
    plt.title(f'Top {top_n} News Sources by Number of Articles')
    plt.show()
