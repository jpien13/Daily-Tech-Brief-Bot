import openai
from config import OPENAI_API_KEY
from user_preferences import preferences
from article_scraper import scrape_articles

openai.api_key = OPENAI_API_KEY

def summarize_articles(articles_content):
    summaries = []
    for article in articles_content:
        # Estimate the number of tokens in the article
        article_tokens = len(article.split())
        available_tokens_for_completion = 4097 - article_tokens

        # Ensure we don't exceed the model's limit
        completion_tokens = min(preferences['summary_length'] * 5, available_tokens_for_completion)

        try:
            response = openai.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=f"Summarize this event in {preferences['summary_length']} words:\n\n{article} emphasizing key points. If there are technical explanations in the article, explain it in a simple way that retains the complexity of the information. The goal is to keep me up to date with events in tech.",
                temperature=0.5,
                max_tokens=completion_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            summaries.append(response.choices[0].text.strip())
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