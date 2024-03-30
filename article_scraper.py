import requests
from bs4 import BeautifulSoup
import time
from typing import List, Union
from urllib.parse import urlparse

class ArticleScraper:
    def __init__(self, urls: List[str]):
        """
        Initializes an instance of the ArticleScraper class.
        Accepts a list of URLs (urls) to scrape.
        Sets a User-Agent in the headers to mimic a real web browser, which helps avoid being blocked by websites.
        """

        self.urls = urls
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    def fetch_article(self, url: str) -> Union[str, None]:
        """
        Fetches an article and extracts content.
        
        Tries to fetch the HTML content of an article by making a GET request to the given URL.
        Uses the User-Agent header set in the __init__ method. If the request is successful, 
        it returns the HTML content as a string; otherwise, it returns None and prints an error message.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_content(self, html: str) -> str:
        """
        Parses HTML content to extract relevant article text.
        
        Looks for the main article container using a list of common selectors 
        ('article', 'main', '.post-content', 'div'). Once the main content is found,
        it extracts all paragraphs (<p> tags) and joins them into a single string.
        """
        soup = BeautifulSoup(html, 'html.parser')
        # Attempt to find the main article container more broadly
        for selector in ['article', 'main', '.post-content', 'div', '.content', 'section', '.text']:
            content = soup.select_one(selector)
            if content:
                paragraphs = content.find_all(['p', 'li', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                return '\\n'.join(p.get_text() for p in paragraphs if p.get_text().strip() != '')
        return ""

    def scrape(self) -> List[str]:
        """
        Main method to scrape articles.
        
        The main method that orchestrates the scraping process.
        Iterates through each URL in the list, fetches the HTML content, 
        and then parses it to extract the article's text.
        Includes a time.sleep(1) call between requests to be respectful to the 
        server's resources. Returns a list containing the text of each article. 
        """
        articles_content = []
        for url in self.urls:
            print(f"Processing {url}")
            html = self.fetch_article(url)
            if html:
                article_text = self.parse_content(html)
                articles_content.append(article_text)
                time.sleep(1)  # Sleep to be polite to the server
            else:
                articles_content.append("")
        return articles_content

def scrape_articles(urls):
    scraper = ArticleScraper(urls)
    return scraper.scrape()

# Example usage for testing
if __name__ == "__main__":
    """ RETURNS A LIST WHERE EACH ELEMENT IS A LONG STRING FOR EACH ARTICLE IN THE ARTICLES LIST"""
    urls = ["https://www.ai21.com/jamba?utm_source=tldrai/1/0100018e8a609272-a5868679-d93b-4b21-b927-2e712c01c2c6-000000/0nEMLp6-F5LE0zznTWamxuLZL65HIvsod-49mCcnhss=346", "https://searchengineland.com/google-starts-testing-ai-overviews-from-sge-in-main-google-search-interface-438680?utm_source=tldrai"]
    scraper = ArticleScraper(urls)
    articles = scraper.scrape()
    for article in articles:
        print(article[:20000])  # Print first 20,000 characters of each article for preview
