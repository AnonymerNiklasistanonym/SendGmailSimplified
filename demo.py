from SendGmailSimplified import SimplifiedGmailApi


# Send for demo uses emails to you or someone else:
yourEmailAddress = "enterHereYourEmailAddress@gmail.com"


"""
Setup line:
"""

# Replace the placeholders and enter your paths like the README.md says
DemoServer = SimplifiedGmailApi("gmail_api_files/client_data.json", "gmail_api_files/client_secret.json", "gmail_api_files")


"""
Send normal text/HTML emails:
"""

# Send a plain text message
DemoServer.send_plain(yourEmailAddress, "Test-Plain-Subject", "1,2,3,4...\nTest, test")

# Send a HTML text message
DemoServer.send_html(yourEmailAddress, "Test-HTML-Subject", "<html><body>1,2,3,4...\nTest, test</body></html>")


"""
Send emails with attachments:
(Currently only working on python 2.* not python 3.*)
"""

# Enter a path to a file (< 25mb) that you want to attach
attachment = "demo.py"

# Send a plain text message with attachments
DemoServer.send_plain_with_attachment(yourEmailAddress, "Test-Plain-With-Attachment-Subject", "1,2,3,4...\nTest, test", attachment)


# Enter paths to files (< 25mb) that you want to attach
attachments = ["demo.py", "SendGmailSimplified.py"]

# Send a HTML text message with attachments
DemoServer.send_html_with_attachments(yourEmailAddress, "Test-HTML-With-Attachments-Subject", "<html><body>1,2,3,4...\nTest, test</body></html>", attachments)


"""
Bonus: Send any or in this case a HTML text message to more than one person
(by using a list and ', '.join(list))
"""

# Enter another email address
anotherEmailAddress = "anotherCool@email.com"

# Add all recipients to a list
email_list = [yourEmailAddress, anotherEmailAddress]

# Add the list with ', '.join(list) instead of a single email address
DemoServer.send_html(', '.join(email_list), "Test-HTML-Multiple-Recipients-Subject", "<html><body>1,2,3,4...\nTest, test</body></html>")