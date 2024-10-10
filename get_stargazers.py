import requests
import json
import logging
from config import GITHUB_API, GITHUB_TOKEN

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_stargazers():
    stargazers = []
    page = 1
    
    # Load existing stargazers from the JSON file
    try:
        with open('stargazers.json', 'r') as infile:
            existing_stargazers = json.load(infile)
            existing_stargazers_dict = {stargazer['id']: stargazer for stargazer in existing_stargazers}
    except FileNotFoundError:
        existing_stargazers_dict = {}
    except json.JSONDecodeError as e:
        logging.error(f"error loading stargazers.json: {e}")
        return []
    
    # Fetch all stargazers from the API, including new ones
    # This approach ensures we don't miss any stargazers while preserving existing data
    while True:
        headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
        response = requests.get(f"{GITHUB_API}?page={page}&per_page=100", headers=headers)
        if response.status_code != 200:
            logging.error(f"error fetching stargazers: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        logging.info(f"fetched {len(data)} stargazers on page {page}")
        
        for stargazer in data:
            existing_stargazers_dict[stargazer['id']] = stargazer
        
        page += 1
        if len(data) < 100:  # Last page
            break
    
    stargazers = list(existing_stargazers_dict.values())
    logging.info(f"total stargazers fetched: {len(stargazers)}")
    
    try:
        with open('stargazers.json', 'w') as outfile:
            json.dump(stargazers, outfile, indent=4)
    except Exception as e:
        logging.error(f"error saving stargazers.json: {e}")
    
    return stargazers