import pandas as pd
import os

class NewsDataLoader:
    '''
    News data IO class.

    This class handles the loading and processing of news data files.

    The data is organized by articles, including metadata such as the article title,
    description, and publication date.

    '''
    def __init__(self, path):
        '''
        path: path to the directory containing news data files
        '''
        self.path = path
        self.articles = self.get_articles()

    def get_articles(self):
        '''
        Function to load articles from the CSV file.
        '''
        file_path = os.path.join(self.path, 'data.csv')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        articles = pd.read_csv(file_path)
        return articles

    def get_articles_by_category(self, category):
        '''
        Function to get articles filtered by a specific category.
        '''
        filtered_articles = self.articles[self.articles['category'] == category]
        return filtered_articles

    def get_top_websites_by_article_count(self, top_n=10):
        '''
        Function to get top N websites by the number of articles.
        '''
        top_websites = self.articles['source_name'].value_counts().head(top_n)
        return top_websites

    def get_highest_traffic_websites(self, traffic_data_path, top_n=10):
        '''
        Function to get top N websites by traffic from the traffic data file.
        '''
        traffic_data = pd.read_csv(traffic_data_path)
        merged_data = pd.merge(self.articles, traffic_data, left_on='source_name', right_on='Domain', how='left')
        highest_traffic_websites = merged_data[['source_name', 'GlobalRank']].dropna().sort_values(by='GlobalRank').head(top_n)
        return highest_traffic_websites

    def get_articles_by_sentiment(self, sentiment):
        '''
        Function to get articles filtered by sentiment.
        '''
        filtered_articles = self.articles[self.articles['title_sentiment'] == sentiment]
        return filtered_articles

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Load and analyze news data')

    parser.add_argument('--data-path', help="Path to the directory containing news data files", required=True)
    parser.add_argument('--traffic-data-path', help="Path to the global website traffic data file", required=True)
    args = parser.parse_args()

    loader = NewsDataLoader(args.data_path)

    # Example usage
    print("Top websites by article count:")
    print(loader.get_top_websites_by_article_count())

    print("\nWebsites with highest traffic:")
    print(loader.get_highest_traffic_websites(args.traffic_data_path))

    print("\nExample articles with positive sentiment:")
    print(loader.get_articles_by_sentiment('positive').head())
