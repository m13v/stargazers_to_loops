import requests
import logging
from config import LOOPS_API, LOOPS_API_KEY

def add_to_loops(user):
    headers = {
        "Authorization": f"Bearer {LOOPS_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": user["email"],
        "firstName": user["name"].split()[0] if user["name"] else "",
        "lastName": " ".join(user["name"].split()[1:]) if user["name"] else "",
        "source": "GitHub Stargazer",
        "userGroup": "screen-pipe-stargazers"
    }
    logging.info(f"Adding {user['email']} to Loops")
    response = requests.post(LOOPS_API, headers=headers, json=data)
    if response.status_code == 200:
        logging.info(f"Added {user['login']} to Loops")
    else:
        logging.error(f"Error adding {user['login']} to Loops: {response.status_code}")