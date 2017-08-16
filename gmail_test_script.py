from SendGmailSimplified import SimplifiedGmailApi

# replace the placeholders and enter your paths like the README.md says
GmailServer = SimplifiedGmailApi("gmail_api_files/client_data.json", "gmail_api_files/client_secret.json", "gmail_api_files")
GmailServer.send_plain("yourEmailAddress@gmail.com", "Test-Subject", "1,2,3,4...\nTest, test")