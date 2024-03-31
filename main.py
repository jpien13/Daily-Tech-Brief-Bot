from article_scraper import scrape_articles
from summarizer import summarize_articles
from sms_sender import send_sms_via_email
from sms_sender_telegram import send_telegram_message
from config import USER_PHONE_NUMBER, TELEGRAM_CHATID, TELEGRAM_BOT_API
from email_processor import get_article_links
import schedule
import time
from user_preferences import preferences

def summarize_and_notify():
    """
    Step 1: Fetch new article links from emails
    Step 2: Scrape articles from the fetched links
    Step 3: Summarize the scraped articles
    Step 4: Send summarized articles via SMS
    """
    article_links = get_article_links('jason_pien@brown.edu', 3)
    articles_content = scrape_articles(article_links)
    summaries = summarize_articles(articles_content)
    carrier_gateway = "vtext.com"    # Verison gateway
    recipient_email = f"{USER_PHONE_NUMBER}@{carrier_gateway}"
    send_telegram_message(TELEGRAM_CHATID, "Hey! This is your brief for today:", TELEGRAM_BOT_API)
    for summary in summaries:
        #send_sms_via_email(recipient_email, "Your Daily Tech Brief!", summary)
        send_telegram_message(TELEGRAM_CHATID, summary, TELEGRAM_BOT_API)


if __name__ == "__main__":
    summarize_and_notify()