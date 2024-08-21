import requests
import json
import logging
from config import GITHUB_TOKEN
from add_to_loops import add_to_loops, check_user_existence_by_email

def process_stargazer(stargazer, lock):
    # Check if the loops field indicates the user has already been processed
    if stargazer.get("loops") in ["added", "already in loops", "no valid email exist"]:
        logging.info(f"Skipping user {stargazer.get('login', 'unknown')} as they have already been processed.")
        return
    
    # Check if necessary fields are present before making the request
    if not stargazer.get("url"):
        logging.warning(f"Stargazer {stargazer.get('login', 'unknown')} does not have a URL, skipping.")
        return
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    user_response = requests.get(stargazer["url"], headers=headers)
    if user_response.status_code == 200:
        user_data = user_response.json()
        user_info = {
            "url": user_data.get("url"),
            "email": user_data.get("email"),
            "name": user_data.get("name"),
            "login": user_data.get("login")
        }
        logging.info(f"User info: {user_info}")
        if user_info["url"]:
            try:
                with open('stargazers.json', 'r') as infile:
                    stargazers = json.load(infile)
            except json.JSONDecodeError as e:
                logging.error(f"Error loading stargazers.json: {e}")
                return
            
            for stargazer in stargazers:
                if stargazer["url"] == user_info["url"]:
                    stargazer.update(user_info)
                    if user_info["email"]:
                        if not check_user_existence_by_email(user_info["email"]):
                            add_to_loops(user_info)
                            stargazer["loops"] = "added"
                        else:
                            stargazer["loops"] = "already in loops"
                            logging.info(f"User with email {user_info['email']} already exists in Loops")
                    else:
                        stargazer["loops"] = "no valid email exist"
                        logging.warning("User does not have a valid email, skipping loops addition")
            
            try:
                with lock:  # Ensure only one thread writes to the file at a time
                    with open('stargazers.json', 'w') as outfile:
                        json.dump(stargazers, outfile, indent=4)
            except Exception as e:
                logging.error(f"Error saving stargazers.json: {e}")
    else:
        logging.error(f"Error fetching user data for {stargazer['login']}: {user_response.status_code}: {user_response.text}")