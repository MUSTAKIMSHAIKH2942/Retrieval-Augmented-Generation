import concurrent.futures
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Dictionary of queries and corresponding URLs
queries_urls = {
    'Industry Information': 'https://en.wikipedia.org/wiki/Canoo',
    'Competitors Information': 'https://en.wikipedia.org/wiki/Tesla,_Inc.',
    'Financial Performance': 'https://investors.canoo.com/financial-information/financial-results',
    'Market Trends': 'https://www.nasdaq.com/articles/canoo:-buy-sell-or-hold'
}

# Function to scrape data from a single web link
def scrape_data(link):
    response = requests.get(link)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Request to {link} returned an error: {response.status_code}")

# Custom function to process and structure the raw HTML data
def process_data(html_data, topic):
    soup = BeautifulSoup(html_data, 'html.parser')
    paragraphs = soup.find_all('p')  # Find all paragraph tags
    
    # Extract paragraphs with their index
    data = {'index': [], 'paragraph': []}
    for index, paragraph in enumerate(paragraphs, 1):
        # Only add paragraphs with more than a few characters
        if len(paragraph.get_text().strip()) > 20:
            data['index'].append(index)
            data['paragraph'].append(paragraph.get_text().strip())
    
    return pd.DataFrame(data)

# Function to store DataFrame in a CSV file
def store_data_in_csv(df, filename):
    df.to_csv(filename, index=False)

# Main process
def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(scrape_data, url): topic for topic, url in queries_urls.items()}
        for future in concurrent.futures.as_completed(future_to_url):
            topic = future_to_url[future]
            try:
                html_data = future.result()
                structured_data = process_data(html_data, topic)
                if not structured_data.empty:
                    csv_filename = f"{topic.replace(' ', '_')}.csv"
                    store_data_in_csv(structured_data, csv_filename)
                    print(f"Data for {topic} saved successfully in {csv_filename}.")
                else:
                    print(f"No data extracted for {topic}.")
            except Exception as e:
                print(f"Error processing {topic}: {str(e)}")

if __name__ == "__main__":
    main()
