# -*- coding: utf-8 -*-

"""Demo of the SimplifiedGmailApi"""


from SendGmailSimplified import SimplifiedGmailApi


# Send for demo uses emails to you or someone else:
YOUR_EMAIL_ADDRESS = "enterHereXourEmailAddress@gmail.com"


"""
Setup line:
"""

# Replace the placeholders and enter your paths like the README.md says
DEMO_SERVER = SimplifiedGmailApi("gmail_api_files/client_data.json",
                                 "gmail_api_files/client_secret.json",
                                 "gmail_api_files")


"""
Send normal text/HTML emails:
"""

# Send a plain text message
DEMO_SERVER.send_plain(YOUR_EMAIL_ADDRESS,
                       "Test-Plain-Subject (ÄÖÜäöü%$)",
                       "1,2,3,4...\nTest, test\nÄÖÜäöü%$")

# Send a HTML text message
DEMO_SERVER.send_html(YOUR_EMAIL_ADDRESS,
                      "Test-HTML-Subject (ÄÖÜäöü%$)",
                      "<html><body>1,2,3,4...\nTest, test\nÄÖÜäöü%$</body></html>")


"""
Send emails with attachments:
(Currently only working on python 2.* not python 3.*)
"""

# Enter a path to a file (< 25mb) that you want to attach
ATTACHMENT = "demo.py"

# Send a plain text message with attachments
DEMO_SERVER.send_plain_with_attachment(YOUR_EMAIL_ADDRESS,
                                       "Test-Plain-With-Attachment-Subject",
                                       "1,2,3,4...\nTest, test", ATTACHMENT)


# Enter paths to files (< 25mb) that you want to attach
ATTACHMENTS = [ATTACHMENT, "SendGmailSimplified.py"]

# Send a HTML text message with attachments
DEMO_SERVER.send_html_with_attachments(YOUR_EMAIL_ADDRESS,
                                       "Test-HTML-With-Attachments-Subject",
                                       "<html><body>1,2,3,4...\nTest, test</body></html>",
                                       ATTACHMENTS)


"""
Bonus: Send any or in this case a HTML text message to more than one person
(by using a list and ', '.join(list))
"""

# Enter another email address
ANOTHER_EMAIL_ADDRESS = "anotherCool@email.adress"

# Add all recipients to a list
EMAIL_LIST = [YOUR_EMAIL_ADDRESS, ANOTHER_EMAIL_ADDRESS]

# Add the list with ', '.join(list) instead of a single email address
DEMO_SERVER.send_html(', '.join(EMAIL_LIST),
                      "Test-HTML-Multiple-Recipients-Subject",
                      "<html><body>1,2,3,4...\nTest, test</body></html>")
