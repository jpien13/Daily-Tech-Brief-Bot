import requests
from config import SLACK_BOT_OAUTH

import os
# Access sensitive data from environment variables
SLACK_BOT_OAUTH = os.getenv('SLACK_BOT_OAUTH')

def send_slack_message(message, slack_token, slack_channel):
    """Send a message to Slack using the OAuth token."""
    headers = {
        'Authorization': f'Bearer {slack_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': slack_channel,
        'text': message
    }
    response = requests.post('https://slack.com/api/chat.postMessage', json=data, headers=headers)
    return response.json()

# Test
if __name__ == "__main__":
    slack_channel = "#test"  # Replace this with your channel ID or name
    message = 'Hello! This is your daily summary from Slack Bot.'
    result = send_slack_message(message, SLACK_BOT_OAUTH, slack_channel)
    print(result)
