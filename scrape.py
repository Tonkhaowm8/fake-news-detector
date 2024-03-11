import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool

import requests

def scrape_article(url):
    try:
        # Send a GET request to the URL with a timeout of 10 seconds
        response = requests.get("http://" + url, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all <p> elements
            paragraphs = soup.find_all('p')
            
            # Extract text from all <p> elements
            all_text = "\n".join([p.get_text() for p in paragraphs])
            
            return all_text
        else:
            print(f"Failed to fetch data from {url}")
            return None
    except requests.Timeout:
        print(f"Request to {url} timed out")
        return None
    except Exception as e:
        print(f"Error scraping URL {url}: {e}")
        return None


def split_by_newline(data):
    if data is None:
        return None
    
    # Remove newline characters that occur before splitting
    data = data.replace('\xa0', '')
    data = data.replace('.\n', '. ')
    data = data.replace('. \n', '. ')
    data = data.replace(".'\n", ".' ")
    data = data.replace('."\n', '." ')
    data = data.replace('"\n', '" ')
    data = data.replace("'\n", "' ")
    data = data.replace('\n"', ' "')
    data = data.replace("’\n", "’ ")
    data = data.replace('\n‘', ' ‘')
    data = data.replace('\t', '\n')

    # Split data by newline characters
    data_array = data.split('\n')
    
    # Remove leading and trailing whitespaces from each item in the array
    data_array = [item.strip() for item in data_array]
    
    # Remove empty strings from the list
    data_array = list(filter(None, data_array))

    return data_array

def save_to_json(data_array, file_path):
    with open(file_path, 'a') as file:
        json.dump(data_array, file)
        file.write('\n')

def process_row(row):
    try:
        url = row['news_url']
        title = row['title']
        scraped_content = scrape_article(url)

        if scraped_content is None:
            # If scraping fails, return None
            return None

        splitData = split_by_newline(scraped_content)
        
        splitData.append([url, title])

        # Return nested list for each row with news_url and title at the beginning
        return splitData
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

def main():
    # Path to your CSV file containing links
    csv_file = os.path.join('csvs', 'test.csv')
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Convert DataFrame to list of dictionaries
    rows = df.to_dict(orient='records')

    # Total number of rows
    total_rows = len(rows)

    # Define the number of processes to use
    num_processes = 6  # Use 6 CPU cores

    # Create a Pool of worker processes
    with Pool(num_processes) as pool:
        # Initialize an empty list to store results from all processes
        all_results = []

        # Initialize progress counter
        processed_count = 0

        # Iterate through each row in the DataFrame
        for i, result in enumerate(pool.imap_unordered(process_row, rows), 1):
            # Update progress count
            processed_count += 1

            # Calculate progress percentage
            progress_percent = (processed_count / total_rows) * 100

            # Print progress
            print(f"Progress: {progress_percent:.2f}% done", end='\r')

            if result is not None:
                # Extend the all_results list with the result
                all_results.append(result)
    
    # Save the all_results list to a single JSON file
    save_to_json(all_results, 'scraped_data.json')
    
    print("\nScraping completed.")

if __name__ == "__main__":
    main()

