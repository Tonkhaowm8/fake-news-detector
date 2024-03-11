import json
import os
import pandas as pd

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def check(data, df, filename):
    authors = ["author", "biographer", "columnist", "creator", "journalist", "producer", "reporter", "writer"]
    dates = [
    "January", "February", "March", "April", 
    "May", "June", "July", "August", 
    "September", "October", "November", "December"]
    author = "-NO AUTHOR-"
    date = ""
    text = ""
    label = ""

    if "fake" in filename:
        label = "Fake"
    else:
        label = "Real"

    for item in data:
        # print(item)
        test = str(item)
        if len(test.replace(" ", "")) > 100:
            text += f"{item} "
        for i in authors:
            if i in item:
                author = item
            else:
                pass
        for j in dates:
            if j in item:
                date = item
            else:
                pass

    df = df.concat({
        'author': author,
        'published': date,
        'title': data[-1][1],
        'text': text,
        'language': "english",
        'site_url': data[-1][0],
        'type': 'bias',
        'label': label,
        'title_without_stopwords': None,
        'text_without_stopwords': None,
        'hasImage': 1}, ignore_index = True)
    
    return df

def main():
    # Create a new pandas dataframe
    df = pd.DataFrame(columns=['author', 'published', 'title', 'text', 'language', 'site_url', 'main_img_url', 'type', 'label', 'title_without_stopwords', 'text_without_stopwords', 'hasImage'])

    directory = 'json'  # Assuming your JSON files are in a directory named 'json'
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            data = read_json_file(file_path)
            if data is not None:
                for i in data:
                    check(i, df, filename)
    
    print(df)
if __name__ == "__main__":
    main()
