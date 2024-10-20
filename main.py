from article_scraper import scrape_articles
from summarizer import summarize_articles
from sms_sender import send_sms_via_email
from sms_sender_telegram import send_telegram_message
from sms_sender_slack import send_slack_message
from config import USER_PHONE_NUMBER, TELEGRAM_CHATID, TELEGRAM_BOT_API
from config import SLACK_BOT_OAUTH
from email_processor import get_article_links
from user_preferences import preferences

def estimate_tokens(text):
    """Estimates the number of tokens in a text."""
    # The average length of tokens in the English language for GPT-like models can be approximated.
    # This is a rough approximation and may not perfectly align with OpenAI's tokenizer.
    AVG_CHARS_PER_TOKEN = 4
    return len(text) / AVG_CHARS_PER_TOKEN

def trim_articles_to_token_limit(articles, token_limit=4097):
    """
    Trims a list of articles to stay under a specified token limit.
    Removes articles from the end until the total token count is within the limit.
    """
    total_tokens = sum(estimate_tokens(article) for article in articles)
    
    # Remove articles from the list until the total token count is under the limit
    while total_tokens > token_limit and articles:
        removed_article = articles.pop()  # Remove the last article
        total_tokens -= estimate_tokens(removed_article)  # Update total token count
    
    return articles

def summarize_and_notify():
    """
    Step 1: Fetch new article links from emails
    Step 2: Scrape articles from the fetched links
    Step 3: May have to truncate the number of articles based on token limits
    Step 4: Summarize the scraped articles
    Step 5: Send summarized articles via SMS
    """
    article_links = get_article_links('dan@tldrnewsletter.com')
    #article_links = get_article_links('pien.jason@gmail.com')

    articles_content = scrape_articles(article_links)
    for article in articles_content:
       print(article)
       print("#############################")
    trimmed_articles = trim_articles_to_token_limit(articles_content, 4097)
    summaries = summarize_articles(trimmed_articles)
    #carrier_gateway = "vtext.com"    # Verison gateway
    #recipient_email = f"{USER_PHONE_NUMBER}@{carrier_gateway}"
    if len(summaries) > 0:
        #send_telegram_message(TELEGRAM_CHATID, "Hey! It's T.I.D.A.L 🌊 giving you your daily updates in tech 🚀🚀🚀! (Loading Content...)", TELEGRAM_BOT_API)
        send_slack_message("Hey! It's T.I.D.A.L giving you your daily updates in tech! (Loading Content...)", SLACK_BOT_OAUTH,"#test")
    else:
        #send_telegram_message(TELEGRAM_CHATID, "😅 Whoops! I've got nothing for you right now. Either I was unable to extract any content today or this was a hiccup! Sorry ", TELEGRAM_BOT_API)
        send_slack_message("Whoops! I've got nothing for you right now. Either I was unable to extract any content today or this was a hiccup! Sorry ", SLACK_BOT_OAUTH, "#test")

    for summary in summaries:
        #send_sms_via_email(recipient_email, "Your Daily Tech Brief!", summary)
        #send_telegram_message(TELEGRAM_CHATID, summary, TELEGRAM_BOT_API)
        send_slack_message(summary, SLACK_BOT_OAUTH, "#test")

if __name__ == "__main__":
    summarize_and_notify()