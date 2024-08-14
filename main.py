import sys
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from process_stargazer import process_stargazer
from get_stargazers import get_stargazers  # Assuming this function exists

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    if len(sys.argv) != 2:
        print("No login provided, fetching all stargazers...")
        get_stargazers()
        with open('stargazers.json', 'r') as infile:
            stargazers = json.load(infile)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(process_stargazer, stargazer): stargazer for stargazer in stargazers}
            for future in as_completed(futures):
                stargazer = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error processing stargazer {stargazer['login']}: {e}")
        return
    
    login = sys.argv[1]
    
    with open('stargazers.json', 'r') as infile:
        stargazers = json.load(infile)
    
    stargazer = next((s for s in stargazers if s["login"] == login), None)
    
    if stargazer:
        print(f"Processing stargazer: {stargazer['login']}")
        process_stargazer(stargazer)
    else:
        print(f"No stargazer found with login: {login}")

if __name__ == "__main__":
    main()