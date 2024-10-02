import sys
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from process_stargazer import process_stargazers
from get_stargazers import get_stargazers
from fix_and_validate_json import validate_json, fix_json_syntax

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    lock = Lock()  # Create a lock for thread-safe file writing
    
    if len(sys.argv) < 2:
        print("Usage: python main.py [login1] [login2] ...")
        print("No login provided, fetching all stargazers...")
        
        # Check if stargazers.json exists
        if not os.path.exists('stargazers.json'):
            logging.info("stargazers.json not found. Fetching stargazers...")
            stargazers = get_stargazers()
            if not stargazers:
                return
        else:
            logging.info("Calling validate_json for stargazers.json")
            if not validate_json('stargazers.json'):
                logging.info("Attempting to fix JSON syntax issues...")
                fix_json_syntax('stargazers.json')
                if not validate_json('stargazers.json'):
                    return
            
            with open('stargazers.json', 'r') as infile:
                stargazers = json.load(infile)
        
        total_stargazers = len(stargazers)
        successful = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=10) as executor:
            chunk_size = len(stargazers) // 10  # Divide stargazers into 10 chunks
            stargazer_chunks = [stargazers[i:i + chunk_size] for i in range(0, len(stargazers), chunk_size)]
            futures = {executor.submit(process_stargazers, chunk, lock): chunk for chunk in stargazer_chunks}
            for future in as_completed(futures):
                chunk = futures[future]
                try:
                    result = future.result()
                    if result:
                        successful += len(chunk)
                    else:
                        failed += len(chunk)
                except Exception as e:
                    logging.error(f"Error processing chunk of stargazers: {e}")
                    failed += len(chunk)

        logging.info(f"processing completed. total: {total_stargazers}, successful: {successful}, failed: {failed}")
        return
    
    else:
        logins = sys.argv[1:]
        
        logging.info("calling validate_json for stargazers.json")
        if not validate_json('stargazers.json'):
            logging.info("attempting to fix json syntax issues...")
            fix_json_syntax('stargazers.json')
            if not validate_json('stargazers.json'):
                return
        
        try:
            with open('stargazers.json', 'r') as infile:
                stargazers = json.load(infile)
        except json.JSONDecodeError as e:
            logging.error(f"error loading stargazers.json: {e}")
            return
        
        stargazers_to_process = [s for s in stargazers if s["login"] in logins]
        
        if stargazers_to_process:
            logging.info(f"processing {len(stargazers_to_process)} existing stargazers")
        else:
            logging.info("no matching stargazers found in existing data. fetching new data...")
            new_stargazers = get_stargazers()
            stargazers_to_process = [s for s in new_stargazers if s["login"] in logins]
            logging.info(f"found {len(stargazers_to_process)} new stargazers to process")
        
        if stargazers_to_process:
            lock = Lock()
            process_stargazers(stargazers_to_process, lock)
        else:
            logging.info("no matching stargazers found after fetching new data")

if __name__ == "__main__":
    main()