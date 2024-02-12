import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Dictionary of queries and corresponding URLs
queries = {
    'Industry Information': 'https://en.wikipedia.org/wiki/Canoo',
    'Competitors Information': 'https://craft.co/canoo/competitors',
    'Market Trends': 'https://www.nasdaq.com/news-and-insights/markets',
    'Financial Performance': 'https://investors.canoo.com/financial-information/financial-results'
}

# Function to scrape data from a single web link
def scrape_data(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

# Function to store data in a CSV file
def store_data_in_csv(data, filename):
    df = pd.DataFrame([data], columns=['text'])
    df.to_csv(filename, index=False)

# Convert the text data to a vector space model
def convert_to_vector_database(text):
    vectorizer = TfidfVectorizer()
    vector_database = vectorizer.fit_transform([text])
    return vector_database, vectorizer

# Function to run queries in the vector space model
def run_queries(query, vector_database, vectorizer):
    query_vector = vectorizer.transform([query])
    cosine_similarities = linear_kernel(query_vector, vector_database).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-5:-1]
    return related_docs_indices

# Text summarization placeholder
def summarize_text(text):
    return text[:100]

# Generate a report file
def generate_report(summary, filename):
    with open(filename, 'w') as f:
        f.write(summary + '\n\n')

# Main process
for query, url in queries.items():
    # Scrape data from the URL
    data = scrape_data(url)
    
    # Store the scraped data in a CSV file
    csv_filename = f"{query.replace(' ', '_')}.csv"
    store_data_in_csv(data, csv_filename)
    
    # Convert the data to a vector space model
    vector_database, vectorizer = convert_to_vector_database(data)
    
    # Run the query in the vector space model
    results_indices = run_queries(query, vector_database, vectorizer)
    
    # For simplicity, we just take the first result to summarize as an example
    if results_indices.size > 0:
        summary = summarize_text(data)
        report_filename = f"{query.replace(' ', '_')}_report.txt"
        generate_report(summary, report_filename)
