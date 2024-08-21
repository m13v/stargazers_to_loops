import sys
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from process_stargazer import process_stargazer
from get_stargazers import get_stargazers
from fix_and_validate_json import validate_json
from fix_and_validate_json import fix_json_syntax

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    lock = Lock()  # Create a lock for thread-safe file writing
    
    if len(sys.argv) != 2:
        print("No login provided, fetching all stargazers...")
        logging.info("Calling validate_json for stargazers.json")
        if not validate_json('stargazers.json'):
            logging.info("Attempting to fix JSON syntax issues...")
            fix_json_syntax('stargazers.json')
            if not validate_json('stargazers.json'):
                return
        
        stargazers = get_stargazers()
        if not stargazers:
            return
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(process_stargazer, stargazer, lock): stargazer for stargazer in stargazers}
            for future in as_completed(futures):
                stargazer = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error processing stargazer {stargazer['login']}: {e}")
        return
    
    login = sys.argv[1]
    
    logging.info("Calling validate_json for stargazers.json")
    if not validate_json('stargazers.json'):
        logging.info("Attempting to fix JSON syntax issues...")
        fix_json_syntax('stargazers.json')
        if not validate_json('stargazers.json'):
            return
    
    try:
        with open('stargazers.json', 'r') as infile:
            stargazers = json.load(infile)
    except json.JSONDecodeError as e:
        logging.error(f"Error loading stargazers.json: {e}")
        return
    
    stargazer = next((s for s in stargazers if s["login"] == login), None)
    
    if stargazer:
        print(f"Processing stargazer: {stargazer['login']}")
        process_stargazer(stargazer, lock)
    else:
        print(f"No stargazer found with login: {login}")

if __name__ == "__main__":
    main()