import requests
import json
import logging
from config import GITHUB_TOKEN
from add_to_loops import add_to_loops, check_user_existence_by_email

def process_stargazers(stargazers, lock):
    updated = False
    processed_count = 0
    for stargazer in stargazers:
        if stargazer.get("loops") in ["added", "already in loops", "no valid email exist"]:
            processed_count += 1
            continue
        result = process_single_stargazer(stargazer)
        if result:
            updated = True
            processed_count += 1
    
    if updated:
        with lock:
            try:
                # Read the existing data
                with open('stargazers.json', 'r') as infile:
                    existing_data = json.load(infile)
                
                # Update the existing data with new information
                for stargazer in stargazers:
                    existing_stargazer = next((s for s in existing_data if s['id'] == stargazer['id']), None)
                    if existing_stargazer:
                        existing_stargazer.update(stargazer)
                    else:
                        existing_data.append(stargazer)
                
                # Write the updated data back to the file
                with open('stargazers.json', 'w') as outfile:
                    json.dump(existing_data, outfile, indent=4)
                logging.info("updated stargazers.json after processing")
            except Exception as e:
                logging.error(f"error updating stargazers.json: {e}")
    
    return processed_count

def process_single_stargazer(stargazer):
    # Check if the loops field indicates the user has already been processed
    if stargazer.get("loops") in ["added", "already in loops", "no valid email exist"]:
        logging.info(f"Skipping user {stargazer.get('login', 'unknown')} as they have already been processed.")
        return False
    
    # Check if necessary fields are present before making the request
    if not stargazer.get("url"):
        logging.warning(f"Stargazer {stargazer.get('login', 'unknown')} does not have a URL, skipping.")
        return False
    
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
        # logging.info(f"User info: {user_info}")
        if user_info["url"]:
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
                # logging.warning("User does not have a valid email, skipping loops addition")
            return True
    else:
        logging.error(f"Error fetching user data for {stargazer['login']}: {user_response.status_code}: {user_response.text}")
    
    return False