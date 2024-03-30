# email_reader.py
from bs4 import BeautifulSoup
import imaplib
import email
import logging
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Configuration
IMAP_SERVER = 'imap.gmail.com'
EMAIL_FOLDER = 'INBOX'

def connect_to_email_server():
    """Establishes connection to the IMAP server and logs in."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select(EMAIL_FOLDER)
        return mail
    except Exception as e:
        logging.error(f"Failed to connect to the email server: {e}")
        raise

def search_for_unread_emails(mail, sender_email):
    """Searches for unread emails from a specific sender."""
    try:
        status, email_ids = mail.search(None, '(UNSEEN FROM "{}")'.format(sender_email))
        if status != 'OK':
            logging.error("No emails found.")
            return []
        return email_ids[0].split()
    except Exception as e:
        logging.error(f"Error searching for emails: {e}")
        raise

def fetch_and_process_emails(mail, email_ids, max_urls=None):
    """Fetches emails by ID and extracts URLs from them based on specified criteria, up to max_urls."""
    links = []
    for e_id in email_ids:
        if max_urls is not None and len(links) >= max_urls:
            break  # Stop if we've collected the max number of links
        
        _, msg_data = mail.fetch(e_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/html":
                            body = part.get_payload(decode=True).decode()
                            new_links = extract_links(body)
                            for link in new_links:
                                if max_urls is not None and len(links) < max_urls:
                                    links.append(link)
                                else:
                                    break
                            if max_urls is not None and len(links) >= max_urls:
                                break  # Exit early if max_urls reached
                else:
                    body = msg.get_payload(decode=True).decode()
                    new_links = extract_links(body)
                    for link in new_links:
                        if max_urls is not None and len(links) < max_urls:
                            links.append(link)
                        else:
                            break
                    if max_urls is not None and len(links) >= max_urls:
                        break  # Exit early if max_urls reached
        if max_urls is not None and len(links) >= max_urls:
            break  # Exit the outer loop if max_urls reached
    return links


def extract_links(html_content):
    """Extracts URLs from the HTML content based on the specified condition."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for a_tag in soup.find_all('a'):
        if 'minute read)' in a_tag.text:
            links.append(a_tag.get('href'))
    return links

def get_article_links(sender_email, max_urls):
    """Orchestrates the process to connect, search, fetch, and process emails, returning up to max_urls links."""
    mail = connect_to_email_server()
    email_ids = search_for_unread_emails(mail, sender_email)
    if email_ids:
        links = fetch_and_process_emails(mail, email_ids, max_urls)
        return links
    else:
        logging.info("No unread emails from the specified sender.")
        return []
