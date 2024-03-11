import json
import os

def read_first_json_entry(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            if data:
                first_entry = data[0]
                return first_entry
            else:
                print("The JSON file is empty.")
                return None
    except FileNotFoundError:
        print("File not found. Please provide a valid JSON file path.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format. Please provide a valid JSON file.")
        return None

# Example usage
json_file_path = os.path.join("json", "gossipcop_fake.json")  # Change this to your JSON file path
first_entry = read_first_json_entry(json_file_path)
if first_entry:
    print("First entry in the JSON file:")
    print(first_entry[-1][0])
