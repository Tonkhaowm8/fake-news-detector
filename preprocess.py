import json
def read_scraped_data(file_path):
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

def main():
    file_path = 'scraped_data.json'
    data = read_scraped_data(file_path)
    if data is not None:
        print("Scraped Data:")
        for item in data:
            print(item)
            print('\n\n\n')

if __name__ == "__main__":
    main()
