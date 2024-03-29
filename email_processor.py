import imaplib                          
import email
from email.header import decode_header
import webbrowser
import os
import re
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

"""
imaplib: This library is used to connect to the IMAP server and execute various 
        IMAP commands, such as logging in and selecting a mailbox.

email and email.header: These are used to parse the emails fetched from the server, 
        allowing you to extract details such as the subject and body.


Script Breakdown:
IMAP Client Setup: The script begins by establishing a secure connection to the Gmail 
                   IMAP server using imaplib.IMAP4_SSL. It then logs in using credentials 
                   stored in config.py.

Email Searching: It selects the 'inbox' mailbox and searches for emails from dan@tldrnewsletter.com. 
                 The mail.search command returns a list of email IDs matching the search criteria.

Email Processing: For each email ID, the script fetches the email using the mail.fetch command 
                  with the '(RFC822)' argument, which is a standard format for the text of an 
                  internet message. The email is then parsed using the email library to extract 
                  and decode the subject and body.

Multipart Emails: Emails can be multipart, meaning they contain different parts (like text and 
                  HTML versions of the message). The script checks if an email is multipart and 
                  iterates over each part, focusing on the 'text/plain' parts for URL extraction.

1. Loop Through Each Email ID

2. Fetch the Email Body
    - the fetch method of the imaplib's mail object to retrieve the email corresponding to the 
      current mail_id. The argument '(RFC822)' specifies that the method should fetch the full 
      email body according to the RFC 822 standard. status captures the operation's status 
      (e.g., 'OK' or 'NO'), and data contains the fetched email data.

3. Iterate Through Each Part of the Fetched Data
    - The fetched email data can contain multiple parts, including the email body, 
      attachments, etc. This line iterates through each part of the data.

4. Check if the Part is a Tuple
    - This condition checks if the current response_part is a tuple. In the context of imaplib, 
      a tuple here usually contains the email header and body.

5. Parse the Email Message
    - This extracts the email message from the second element of the tuple (which contains the 
      email content as bytes) and parses it into an email.message.EmailMessage object.

6. Decode Email Subject
    - The subject of the email is decoded here. Email headers can be encoded in various 
      character sets, so decode_header is used to handle this. If the subject is in bytes, 
      it's decoded using the obtained encoding.

7. Check if Email is Multipart
    - This checks if the email contains multiple parts (e.g., text and HTML versions of the message, attachments).

8. Iterate Over Each Part of the Email
    - For multipart messages, msg.walk() iterates over each part of the email.

9. Extract Text/Plain Content
    - This condition checks if the part's content type is "text/plain". If so, it decodes the payload to get the 
    email body as a string.

10. Extract URLs from the Email Body
    - This line uses a regular expression to find all URLs in the body of the email. The pattern is designed 
      to match http and https URLs.
"""

imap_url = 'imap.gmail.com'
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
mail.select('inbox')

status, messages = mail.search(None, '(UNSEEN FROM "dan@tldrnewsletter.com")')     #messages is a list of email ID's
messages = messages[0].split(b' ')

for mail_id in messages:
    status, data = mail.fetch(mail_id, '(RFC822)')         # Fetch the email body (RFC822) for the given ID
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()       #get email body as a string
                        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
                        print(f"Subject: {subject}")
                        print(f"URLs: {urls}", end="\n\n")
            else:
                body = msg.get_payload(decode=True).decode()
                urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
                print(f"Subject: {subject}")
                print(f"URLs: {urls}", end="\n\n")

    mail.store(mail_id, '+FLAGS', '\Seen')      # Mark the email as read