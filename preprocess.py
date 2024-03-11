import json

def contains_copyright_logo(text):
    return "©" not in text

def filter_data(data):
    filtered_data = [item for item in data if len(item['content']) >= 200 and contains_copyright_logo(item['content'])]
    return filtered_data

def read_scraped_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # print(f"Data Before remove {len(data)}")
            # filtered_data = filter_data(data)
            return data
    except FileNotFoundError:
        print("Error: File not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    file_path = 'scraped_data.json'
    data = read_scraped_data(file_path)
    if data is not None:
        # print("Scraped Data:")
        # print(f"Data After remove {len(data)}")
        for item in data:
            for i in item:
                print(i)
                print('\n\n\n')

if __name__ == "__main__":
    main()
