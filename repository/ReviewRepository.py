import json
import os
import random
import time
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

from matplotlib import pyplot as plt

from repository.TextDataProcessor import TextDataProcessor


class ReviewRepository:

    def load_data_from_given_url(self, url, idx):
        try:
            response = requests.get(url)
            response.raise_for_status()
            print("Repository: Successfully fetched the page.")

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the review elements (example selectors, replace with actual HTML structure)
            reviews = []
            review_elements = soup.find_all('div', class_='product-review-item js-review-item row')
            print("Repository: Successfully got to container.")

            for review_element in review_elements:
                # Add delay to avoid overwhelming the server
                time.sleep(5)

                # Extract and clean title
                title_tag = review_element.find('h3', class_='product-review-title').find('a')
                title = title_tag.text.strip() if title_tag else "No Title"

                # Extract and clean content
                content_tag = review_element.find('div', class_='js-review-body review-body-container')
                content = content_tag.text.strip() if content_tag else "No Content"

                # Extract star rating from class (e.g., "rated-5" -> 5 stars)
                star_rating_container = review_element.find('div', class_='star-rating')
                if star_rating_container:
                    rating_class = star_rating_container.get('class', [])
                    star_rating = int(re.search(r'rated-(\d+)', ' '.join(rating_class)).group(1)) if re.search(
                        r'rated-(\d+)', ' '.join(rating_class)) else 0
                else:
                    star_rating = 0

                # Append structured review data with index and timestamp
                reviews.append({
                    'index': idx,
                    'title': title,
                    'content': content,
                    'starRating': star_rating
                })
                idx+=1
        except requests.RequestException as e:
            print(f"Repository: An error occurred while fetching the page: {e}")
        return reviews,idx

    def scrape_data(self):
        urls = [
            "https://www.emag.ro/laptop-apple-macbook-air-13-inch-cu-procesor-apple-m2-8-nuclee-cpu-si-8-nuclee-gpu-8-gb-256gb-starlight-layout-int-mly13ze-a/pd/D736H4MBM/?ref=other_customers_viewed_go_3_5&provider=rec&recid=rec_52_c989fe46814866263393fb0c207c5aec70fefb99fc15b52caf0f51dae96667e3_1730047706&scenario_ID=52#reviews-section",
            "https://www.emag.ro/laptop-apple-macbook-air-13-inch-true-tone-procesor-apple-m1-8-nuclee-cpu-si-7-nuclee-gpu-8gb-256gb-silver-int-kb-mgn93ze-a/pd/D85BL7MBM/?ref=other_customers_viewed_go_3_2&provider=rec&recid=rec_52_a8d3db3d6b99a55bcdcbf363f81f6de97de46aa66e0745aaa3033974ed7c39c5_1730047714&scenario_ID=52#reviews-section",
            "https://www.emag.ro/televizor-samsung-led-43du7172-108-cm-smart-4k-ultra-hd-clasa-g-model-2024-ue43du7172uxxh/pd/DKRSSPYBM/#reviews-section",
            "https://www.emag.ro/centura-abdominala-postnatala-dublu-reglabila-one-size-6427416001805/pd/DHYXCRMBM/#reviews-section"
        ]

        all_reviews = []
        idx=1

        # Collect reviews from each URL
        for url in urls:
            reviews, idx = self.load_data_from_given_url(url,idx)
            all_reviews.append(reviews)  # Aggregate reviews from each page

        # Save the aggregated reviews to a JSON file
        with open('scraped_reviews.json', 'w', encoding='utf-8') as f:
            json.dump(all_reviews, f, ensure_ascii=False, indent=4)
            print("Repository: Data saved to scraped_reviews.json with reviews from all URLs.")

        return all_reviews

    def load_tabular_data(self):
        print("Repository: Loading and processing tabular data from file...")

        # Define file paths
        input_file = "/filesToUpload/reviews.csv"
        output_file = "C:/Users/Andra Ursa/Desktop/data sceince/dcm/FinalProject/cleaned_reviews.csv"

        # Process data
        processor = TextDataProcessor(input_file, output_file)
        processor.load_and_filter_data()
        processor.clean_content()
        processor.save_processed_data()

        print("Repository: Tabular data processing completed.")

    def call_external_api(self):
        url = "https://jsonplaceholder.typicode.com/posts"

        try:
            # Make the API request
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Modify the data by adding 'starRating' and removing 'userId'
            for entry in data:
                entry['starRating'] = str(random.randint(1, 5))  # Assign a random star rating
                entry.pop('userId', None)  # Remove the 'userId' key if it exists

            # Save modified data to a local JSON file
            with open("fetched_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print("Repository: Data fetched from API, modified, and saved to fetched_data.json.")
            return data  # Return the data if you need it for further processing

        except requests.RequestException as e:
            print(f"Repository: An error occurred while fetching data from API: {e}")
            return None

    def create_visualization(self):
        print("Repository: Creating data visualizations...")

        # Initialize an empty list to store DataFrames
        data_frames = []

        # Load JSON files if they exist
        json_files = ['fetched_data.json', 'processed_data.json', 'scraped_reviews.json']
        for file_name in json_files:
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    df = pd.DataFrame(data)
                    data_frames.append(df)
                    print(f"Repository: Loaded data from {file_name}")

        # Load CSV file if it exists
        csv_file = 'cleaned_reviews.csv'
        if os.path.exists(csv_file):
            df_csv = pd.read_csv(csv_file)
            data_frames.append(df_csv)
            print("Repository: Loaded data from cleaned_reviews.csv")

        # Concatenate all available DataFrames into a single DataFrame
        if not data_frames:
            print("Repository: No data files available for visualization.")
            return
        combined_df = pd.concat(data_frames, ignore_index=True)

        # Ensure 'star_rating' and 'content' fields are present
        if 'starRating' in combined_df.columns:
            combined_df['starRating'] = combined_df['starRating'].fillna(0).astype(int)
        else:
            combined_df['starRating'] = 0

        # Replace NaN in 'content' and convert all values to strings
        combined_df['content'] = combined_df['content'].fillna("").astype(str)

        # Map sentiment based on star ratings
        combined_df['sentiment'] = combined_df['starRating'].apply(
            lambda x: 'Positive' if x >= 4 else ('Negative' if x <= 2 else 'Neutral'))

        # 1. Sentiment Distribution (Pie Chart)
        sentiment_counts = combined_df['sentiment'].value_counts()
        plt.figure(figsize=(6, 6))
        plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Sentiment Distribution')
        plt.savefig('static/sentiment_distribution.png')
        print("Repository: Sentiment distribution pie chart saved as sentiment_distribution.png.")

        # 2. Review Length Distribution (Histogram)
        combined_df['review_length'] = combined_df['content'].apply(len)
        plt.figure(figsize=(10, 6))
        plt.hist(combined_df['review_length'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Review Length Distribution')
        plt.xlabel('Review Length (characters)')
        plt.ylabel('Frequency')
        plt.savefig('static/review_length_distribution.png')
        print("Repository: Review length histogram saved as review_length_distribution.png.")

        # 3. Star Rating Distribution (Histogram)
        plt.figure(figsize=(8, 5))
        plt.hist(combined_df['starRating'], bins=range(1, 7), color='orange', edgecolor='black', align='left')
        plt.title('Star Rating Distribution')
        plt.xlabel('Star Rating')
        plt.ylabel('Frequency')
        plt.xticks(range(1, 6))  # Show only 1 to 5 on the x-axis
        plt.savefig('static/starRating_distribution.png')
        print("Repository: Star rating histogram saved as starRating_distribution.png.")

        # Optional: display plots if running in an interactive environment
        plt.show()

    def load_json_data(self, file):
        save_path = 'processed_data.json'
        try:
            # Load JSON data directly from the uploaded file
            data = json.load(file)
            max_index = 0
            for entry in data:
                try:
                    # Convert index to integer if it's a valid number
                    current_index = int(entry.get('index', 0))
                    max_index = max(max_index, current_index)
                except ValueError:
                    pass  # Ignore non-integer indices

            # Validate and add defaults if fields are missing or empty
            for entry in data:
                # Set 'index' to be the next highest value as a string if missing
                entry.setdefault('index', str(max_index + 1))
                max_index += 1  # Increment max_index for unique indices
                entry.setdefault('title', "Untitled Review")
                entry.setdefault('content', "No content provided")
                entry.setdefault('starRating', "1")

            # Save validated data to the permanent location
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print("Repository: JSON data validated and saved successfully.")

            return data

        except Exception as e:
            print(f"Repository: An error occurred while loading JSON data: {e}")
            raise

    def build_segmentation_model(self):
        '''
        Feature Matrix: We use starRating and review_length as features. Scaling: Standardizes the features using StandardScaler to improve clustering performance.
        K-Means Clustering: Applies K-Means to create clusters. Visualization: Plots the clusters using review_length and starRating.
        Cluster Analysis: Summarizes the characteristics of each cluster, including the average starRating and review_length and the number of reviews.
        :return:
        '''
        print("Repository: Building segmentation model...")

        # Load and combine data as before
        data_frames = []
        json_files = ['fetched_data.json', 'processed_data.json', 'scraped_reviews.json']
        for file_name in json_files:
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    df = pd.DataFrame(data)
                    data_frames.append(df)
                    print(f"Repository: Loaded data from {file_name}")

        csv_file = 'cleaned_reviews.csv'
        if os.path.exists(csv_file):
            df_csv = pd.read_csv(csv_file)
            data_frames.append(df_csv)
            print("Repository: Loaded data from cleaned_reviews.csv")

        if not data_frames:
            print("Repository: No data files available for clustering.")
            return
        combined_df = pd.concat(data_frames, ignore_index=True)

        # Preprocess data
        combined_df['starRating'] = combined_df['starRating'].fillna(0).astype(int)
        combined_df['review_length'] = combined_df['content'].fillna("").apply(len)

        # Create a feature matrix for clustering
        features = combined_df[['starRating', 'review_length']].values
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)  # Adjust the number of clusters as needed
        combined_df['cluster'] = kmeans.fit_predict(scaled_features)

        # Visualize the clusters
        plt.figure(figsize=(10, 6))
        for cluster in np.unique(combined_df['cluster']):
            plt.scatter(
                combined_df[combined_df['cluster'] == cluster]['review_length'],
                combined_df[combined_df['cluster'] == cluster]['starRating'],
                label=f"Cluster {cluster}"
            )
        plt.xlabel('Review Length')
        plt.ylabel('Star Rating')
        plt.title('Clusters of Reviews')
        plt.legend()
        plt.savefig('static/review_clusters.png')
        print("Repository: Cluster visualization saved as review_clusters.png.")

        # Analyze characteristics of each group
        cluster_summary = combined_df.groupby('cluster').agg({
            'starRating': 'mean',
            'review_length': 'mean',
            'content': 'count'
        }).rename(columns={'content': 'review_count'})
        print("Repository: Cluster analysis summary:\n", cluster_summary)

        # Return the summary if needed for further analysis
        return cluster_summary
