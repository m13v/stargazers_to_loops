import sys
import json
import logging
from process_stargazer import process_stargazer
from get_stargazers import get_stargazers  # Assuming this function exists

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    if len(sys.argv) != 2:
        print("No login provided, fetching all stargazers...")
        get_stargazers()
        with open('stargazers.json', 'r') as infile:
            stargazers = json.load(infile)
        
        for stargazer in stargazers:
            print(f"Processing stargazer: {stargazer['login']}")
            process_stargazer(stargazer)
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