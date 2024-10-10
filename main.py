import sys
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from process_stargazer import process_stargazers
from get_stargazers import get_stargazers
from fix_and_validate_json import validate_json, fix_json_syntax

def merge_stargazers(existing, new):
    merged = {s['id']: s for s in existing}
    for stargazer in new:
        if stargazer['id'] not in merged:
            merged[stargazer['id']] = stargazer
        else:
            merged[stargazer['id']].update(stargazer)
    return list(merged.values())

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    lock = Lock()  # Create a lock for thread-safe file writing
    
    if len(sys.argv) < 2:
        print("Usage: python main.py [login1] [login2] ...")
        print("No login provided, fetching all stargazers...")
        
        # Always fetch new stargazers
        logging.info("fetching new stargazers...")
        new_stargazers = get_stargazers()
        
        if os.path.exists('stargazers.json'):
            logging.info("merging with existing stargazers...")
            if validate_json('stargazers.json'):
                with open('stargazers.json', 'r') as infile:
                    existing_stargazers = json.load(infile)
                stargazers = merge_stargazers(existing_stargazers, new_stargazers)
            else:
                logging.warning("existing stargazers.json is invalid, using only new data")
                stargazers = new_stargazers
        else:
            stargazers = new_stargazers
        
        # Save merged stargazers
        with open('stargazers.json', 'w') as outfile:
            json.dump(stargazers, outfile, indent=4)
        
        total_stargazers = len(stargazers)
        successful = 0
        failed = 0

        with ThreadPoolExecutor(max_workers=10) as executor:
            stargazers_to_process = [s for s in stargazers if s.get("loops") not in ["added", "already in loops", "no valid email exist"]]
            chunk_size = len(stargazers_to_process) // 10  # Divide stargazers into 10 chunks
            stargazer_chunks = [stargazers_to_process[i:i + chunk_size] for i in range(0, len(stargazers_to_process), chunk_size)]
            futures = {executor.submit(process_stargazers, chunk, lock): chunk for chunk in stargazer_chunks}
            for future in as_completed(futures):
                chunk = futures[future]
                try:
                    processed = future.result()
                    successful += processed
                    failed += len(chunk) - processed
                except Exception as e:
                    logging.error(f"error processing chunk of stargazers: {e}")
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