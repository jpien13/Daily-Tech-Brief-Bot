import requests
import os
# Access sensitive data from environment variables
TELEGRAM_BOT_API = os.getenv('TELEGRAM_BOT_API')
TELEGRAM_CHATID = os.getenv('TELEGRAM_CHATID')



def send_telegram_message(chat_id, message, bot_token):
    send_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(send_url, data=params)
    return response.json()

# Test
if __name__ == "__main__":
    bot_token = TELEGRAM_BOT_API
    chat_id = TELEGRAM_CHATID
    message = 'Hello! This is your daily summary from Telegram Bot.'
    result = send_telegram_message(chat_id, message, bot_token)
    print(result)
