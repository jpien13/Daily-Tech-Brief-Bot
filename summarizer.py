import openai
import os
from user_preferences import preferences
from article_scraper import scrape_articles

# Access sensitive data from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

def estimate_tokens(text):
    """Estimates the number of tokens in a text."""
    AVG_CHARS_PER_TOKEN = 4  # Rough approximation for GPT-like models
    return len(text) / AVG_CHARS_PER_TOKEN

def summarize_articles(articles_content):
    summaries = []
    for article in articles_content:
        # Estimate the number of tokens in the article
        article_tokens = estimate_tokens(article)

        # Set a safe minimum for available tokens
        available_tokens_for_completion = max(0, 4097 - article_tokens)

        # Ensure we calculate `completion_tokens` correctly
        completion_tokens = min(preferences['summary_length'] * 5, available_tokens_for_completion)

        try:
            response = openai.Completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=f"Summarize this event in {preferences['summary_length']} words:\n\n{article} emphasizing key points.",
                temperature=0.5,
                max_tokens=completion_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            summaries.append(response.choices[0].text.strip())
        except openai.error.APIConnectionError as e:
            print(f"OpenAI API connection error: {e}")
            summaries.append("Error summarizing article: could not process due to connection.")
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request to OpenAI API: {e}")
            summaries.append("Error summarizing article: request parameters invalid.")
        except openai.error.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            summaries.append("Error summarizing article: could not process.")
    return summaries

if __name__ == "__main__":

    urls = ["https://www.theverge.com/2024/3/28/24112507/sam-bankman-fried-sentence-ftx-alameda", "https://arstechnica.com/gadgets/2024/03/netflix-ad-spend-led-to-facebook-dm-access-end-of-facebook-streaming-biz-lawsuit/?utm_source=tldrnewsletter"]
    articles_content = scrape_articles(urls)
    summaries = summarize_articles(articles_content)
    for i, summary in enumerate(summaries, 1):
        print(f"Summary {i}:", summary, "\n")