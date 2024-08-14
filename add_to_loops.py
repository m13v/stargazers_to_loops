import requests
import logging
from config import LOOPS_API, LOOPS_API_KEY
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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
    
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    try:
        response = session.post(LOOPS_API, headers=headers, json=data)
        response.raise_for_status()
        logging.info(f"Successfully added {user['email']} to Loops")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to add {user['email']} to Loops: {e}")

def check_user_existence_by_email(email):
    headers = {
        "Authorization": f"Bearer {LOOPS_API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"https://app.loops.so/api/v1/contacts/find?email={email}"
    logging.info(f"Checking existence of user with email {email} at {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contacts = response.json()
        if contacts:
            # logging.info(f"User with email {email} exists in Loops")
            return True
        else:
            logging.info(f"User with email {email} does not exist in Loops")
            return False
    else:
        logging.error(f"Error checking user existence: {response.status_code} - {response.text}")
        return False