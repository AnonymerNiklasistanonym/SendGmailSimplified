# SendGmailSimplified
Send with only 3 lines of python code an email over the official Gmail API. Easy to add and simple to use. Attachments only supported on python 2.

**Virtual environment:** [How to setup and use `virtualenv` to run this script](VIRTUALENV.md)



## What is this API?

This python API is nothing new or groundbreaking. I just wanted to send an email with the official Gmail API with nothing but 2 Lines in the code and one import in python.

This could make and made my python `Cron` job scripts, which check different things over the day really effective, because I can now very easy integrate the Gmail API and send notification or emails within one line anywhere in the script.

I connected with some people and read the official Google Documentation and... now you and everyone can use an optimize it (MIT license).

Have fun!



**Attention:**

It seems like the current version is only fully supported on python 2.* (tested with 2.7.13 on my Raspberry Pi 3).
If you are on python 3.* only plain text or html text without attachments will work.



## Instructions

(Source: [Google Developers Gmail API Python](https://developers.google.com/gmail/api/quickstart/python))

### 0. Create or Have a Google account

Obviously you first need a Google account and logged into Gmail for once to set up everything.

### 1. Google Developer Console setup

Visit the [Google API website](https://console.developers.google.com/start/api?id=gmail) and create a new Project:

- Click `Select a project` at the top left (after you logged in with your Google account)
  - Then named it and press continue on the next page
- After some time the API is activated and a button `Go to credentials` will appear
  - Simple: Click `Cancel` at the bottom of the page
- Now you will find yourself in a tab interface
  - Click the tab which is named `OAuth consent screen`
    - Select the right email address
    - Enter the name of your project/service/product
    - You can do more but for now you are ready and can press `Save`
  - Back in the tab interface click the tab which is named `Credentials`
    - Now we want to create credentials and therefore expand the button `Create credentials` by clicking the triangle
    - Now let's click the entry `OAuth client ID`
      - Choose there your application type
        (I chose `Other` and entered the name of my service + "ClientID")
    - Now a small window will pop up which we will instantly dismiss
      (by clicking `OK`)
  - But because we want the client ID we'll download the JSON file of the created client ID:
    - Just click the arrow down next to the client ID entry (:arrow_down:)

Now you have the necessary file with which we can set up the Gmail API.

### 2. Set up the Gmail API

The following steps will be really easy:

- Rename the downloaded JSON file to `client_secret.json`

Copy the file to a desired directory of yourself.

Create another JSON file (just copy the following code in a text file and rename it `client_data.json`):

```json
{
	"email": "yourMailAdresse@gmail.com",
	"email-name": "Your Name",
	"application-name": "Previous created service name",
	"permission-scope": "https://www.googleapis.com/auth/gmail.send"
}
```

Edit the file as following:

- replace the placeholders for everything but the `permission-scope` line with your data
- copy the file to another desired directory of yourself
  (if you want it simple put it in the same directory)

### 3. Install the Google API python client

Therefore just open the console and enter:

```
$ pip install --upgrade google-api-python-client
```

And confirm if you didn't sudo'd.

### 4. Activate the API in your python script

This is even simpler.

You now just need three lines to activate and test the API:

```python
from SendGmailSimplified import SimplifiedGmailApi

GmailServer = SimplifiedGmailApi("gmail_api_files/client_data.json", "gmail_api_files/client_secret.json", "gmail_api_files")
GmailServer.send_plain("enterHereYourEmailAddress@gmail.com", "Test-Subject", "1,2,3,4...\nTest, test")
```

The three paths are:

| Path to `client_data.json`           | Path to `client_secret.json`           | Directory of [future] API file |
| ------------------------------------ | -------------------------------------- | ------------------------------ |
| `"gmail_api_files/client_data.json"` | `"gmail_api_files/client_secret.json"` | `"gmail_api_files"`            |

Now execute the script.

- A browser window should open itself and ask you to login with your Google account
- Then allow the API to `Send email on your behalf` over your account

After you clicked `Allow` the necessary file is automatically saved into the directory on your computer of your third parameter.

If you didn't get an email look in the console.
Probably you find something like `403 - Message could not be send`.

But this is not a problem: Just click like the official Gmail API says on the link just to get forwarded back to the API Developer Console.
Then you do what the text says (at least for me) and click `Enable`.
Now run the script again.



## Demo

If you want a fast start into how to use the API just take a look into the [`demo.py`](demo.py) script:

```python
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
```

Just input your email and change all attachment paths to real files + replace the paths in line 8 and you are good to go. (Run it and you will see it).



## How can you use it in your project as git submodule?

If you generally wanna know how to do it visit this site: https://github.com/blog/2104-working-with-submodules

1. Open the console in the directory where you want to place the folder with all files from this repository

2. Then enter:

   ```
   $ git submodule add https://github.com/AnonymerNiklasistanonym/SendGmailSimplified SimplifiedGmailApiSubmodule
   ```

3. If you want to use it in a script which is located in the same directory just add:

   ```python
   from SimplifiedGmailApiSubmodule.SendGmailSimplified import SimplifiedGmailApi
   ```

4. Now you can use the script like in the Demo

5. If any updates be released and you want to update the submodule use:

   ```
   $ git submodule update --init --recursive
   ```



## Problems, ideas?

- If this didn't worked for you message me, make an Issue and we try to help if we have time.
- If you have any ideas, optimizations please message me too (or open a issue/pull-request).





## Last words

We hope this API simplifies sending an email to someone with the official Gmail API without any headaches and many lines of code.

Thanks for using this simple API and have fun programming!
