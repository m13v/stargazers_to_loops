import requests
import logging
from config import LOOPS_API_KEY

def read_emails_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def update_subscription_status(email, subscribed=True):
    headers = {
        "Authorization": f"Bearer {LOOPS_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "subscribed": subscribed
    }
    url = "https://app.loops.so/api/v1/contacts/update"
    
    logging.info(f"updating {email} subscription status to {subscribed}")
    
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        logging.info(f"successfully updated {email} subscription status to {subscribed}")
    except requests.exceptions.RequestException as e:
        logging.error(f"failed to update {email} subscription status: {e}")

def update_batch_subscriptions(emails):
    for email in emails:
        update_subscription_status(email, True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    emails_to_subscribe = read_emails_from_file('subscribed2unsubscribed')
    logging.info(f"loaded {len(emails_to_subscribe)} emails from file")
    
    update_batch_subscriptions(emails_to_subscribe)