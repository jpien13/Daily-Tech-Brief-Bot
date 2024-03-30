import schedule
import time
from summarizer import summarize_and_notify  # Assuming you have this function set up to summarize and send notifications
from user_preferences import preferences

def job():
    print("Fetching, summarizing articles, and sending notifications...")
    summarize_and_notify()  # Your function to fetch, summarize, and notify

# Schedule the job based on user preference
schedule.every().day.at(preferences['notification_time']).do(job)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
