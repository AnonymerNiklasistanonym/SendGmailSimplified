from SendGmailSimplified import SimplifiedGmailApi

# send for demo uses emails to you or someone else:
yourEmailAddress = "niklas.mikeler@gmail.com"

# replace the placeholders and enter your paths like the README.md says
DemoServer = SimplifiedGmailApi("gmail_api_files/client_data.json", "gmail_api_files/client_secret.json", "gmail_api_files")

# Send a plain text message
DemoServer.send_plain(yourEmailAddress, "Test-Subject", "1,2,3,4...\nTest, test")

# Send a HTML text message
DemoServer.send_plain(yourEmailAddress, "Test-Subject", "<html><body>1,2,3,4...\nTest, test</body></html>")

# Enter a path to a file (< 25mb) that you want to attach
attachment = "SendGmailSimplified.py"
# Send a plain text message with attachments
DemoServer.send_plain_with_attachment(yourEmailAddress, "Test-Plain-With-Attachment", "1,2,3,4...\nTest, test", attachment)

# Enter paths to files (< 25mb) that you want to attach
attachments = ["test.m4a", "beta.txt", "test.py", "SendGmailSimplified.py"]
# Send a HTML text message with attachments
DemoServer.send_html_with_attachments(yourEmailAddress, "Test-HTML-With-Attachments", "<html><body>1,2,3,4...\nTest, test</body></html>", attachments)