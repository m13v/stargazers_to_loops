import json
from collections import Counter

def filter_and_print(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        
        total_records = len(data)
        records_with_loops = [record for record in data if 'loops' in record]
        loops_counter = Counter(record['loops'] for record in records_with_loops if record['loops'] is not None)
        
        print(f"Total records: {total_records}")
        print(f"Records with 'loops' field: {len(records_with_loops)}")
        print("Breakdown of 'loops' field:")
        for loops_value, count in loops_counter.items():
            print(f"  {loops_value}: {count}")

# Replace 'stargazers.json' with the path to your JSON file
filter_and_print('stargazers.json')