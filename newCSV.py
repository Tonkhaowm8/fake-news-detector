import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    # Send a GET request to the URL
    response = requests.get("https://" + url)
    
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

def extract_author(scraped_content):
    # Parse the scraped content using BeautifulSoup
    soup = BeautifulSoup(scraped_content, 'html.parser')
    
    # Find <meta> tag with property="author" in the <head> section
    author_tag = soup.find('meta', attrs={'property': 'author'})
    
    # If author_tag is found, extract the content attribute
    if author_tag:
        author = author_tag.get('content')
        return author.strip()  # Remove leading and trailing whitespaces
    
    # If author_tag is not found, return None or any other default value
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

    # print(repr(data))
    # print("\n\n\n")
    # print((data))

    # Split data by newline characters
    data_array = data.split('\n')
    
    # Remove leading and trailing whitespaces from each item in the array
    data_array = [item.strip() for item in data_array]
    
    return data_array


def main():
    # Path to your CSV file containing links
    csv_file = os.path.join('csvs', 'gossipcop_fake.csv')
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    
    # Create an empty DataFrame to store scraped content
    scraped_df = pd.DataFrame(columns=['author', 'published', 'title', 'text', 'language', 'site_url', 'main_img_url', 'type', 'label', 'title_without_stopwords', 'text_without_stopwords', 'hasImage'])
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        url = row['news_url']
        scraped_content = scrape_article(url)

        splitData = split_by_newline(scraped_content)
        
        # Find the longest array
        longest_array = max(splitData, key=len)

        scraped_df = scraped_df.append({'author': row['author'], 
                                        'published': row['published'], 
                                        'title': row['title'], 
                                        'text': longest_array, 
                                        'language': "english", 
                                        'site_url': row['site_url'], 
                                        'main_img_url': 0, 
                                        'type': 'bias', 
                                        'label': 'Fake', 
                                        'title_without_stopwords': row['title_without_stopwords'], 
                                        'text_without_stopwords': row['text_without_stopwords'], 
                                        'hasImage': 1}, 
                                        ignore_index=True)
        # print(scraped_content)
        # print(splitData[6])
        # Append scraped content to the DataFrame
        
    
    # Save the DataFrame to a new CSV file
    scraped_csv_file = os.path.join('csvs', 'scraped_data.csv')
    scraped_df.to_csv(scraped_csv_file, index=False)
    print("Scraped data saved to:", scraped_csv_file)

if __name__ == "__main__":
    main()
