# -*- coding: utf-8 -*-

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import base64
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import mimetypes
from email.mime.multipart import MIMEMultipart
import os
from apiclient import errors
import argparse
import logging
import json
import sys


class SimplifiedGmailApi:
    """SendGmailSimplified API
    A simple Gmail API handler class. Use the Gmail API send Email option
    - without many lines to implement in your script (only 3 are needed)
    - and easy to use and easy understand methods
    If you want to know more or have problems visit it on GitHub:
    https://github.com/AnonymerNiklasistanonym/SendGmailSimplified
    """

    def __init__(self,
                 client_data_path, client_secret_path,
                 api_directory=os.path.join(os.path.expanduser('~'), "GmailCredentialsApi")):
        """'Constructor' - Initial setup of the Gmail API.

        Args:
        client_data_path: The path to your client_data.json file. (Read the instructions README.md)
        client_secret_path: The path to your client_secret.json file. (Read the instructions README.md)
        api_directory: The path of the directory where the gmail_api file will be saved.

        """

        # Because of current problems this is true when you use it on a PYTHON_2 computer
        if sys.version_info[0] < 3:
            self.PYTHON_2 = True
        else:
            self.PYTHON_2 = False
            info_text = "You are using Python > 2 -> Therefore you can not send attachments."
            print(info_text)
            logging.warning(info_text)

        # Other support will probably come but everything else is to now not supported!

        self.PATH_FOR_GMAIL_CLIENT_SECRET_FILE = client_secret_path
        # client_secret.json file path (Read the instructions README.md)
        self.DIRECTORY_FOR_GMAIL_API = api_directory
        # directory for the Gmail API file

        # check if the necessary two files for using the API are not None
        if client_data_path is None or client_secret_path is None:
            # >> abort the process if they are
            info_text = ("SimplifiedGmailApi could not be started since necessary parameter are None." +
                         "(client_data_path,  client_secret_path)")
            print(info_text)
            logging.warning(info_text)
            self.SetupOk = False
        elif not os.path.isfile(client_data_path) or not os.path.isfile(client_secret_path):
            # >> abort the process if they are
            info_text = ("SimplifiedGmailApi could not be started since the following files weren't found: ")
            for pathOfFile in [client_data_path, client_secret_path]:
                if not os.path.isfile(pathOfFile):
                    info_text += "\n - " + pathOfFile
            print(info_text)
            logging.warning(info_text)
            self.SetupOk = False
        else:
            # >> if they aren't None load everything from the files and start the API
            self.SetupOk = True

            with open(client_data_path, "r") as credentials_file:
                data_file = json.load(credentials_file)

            try:
                self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
            except ImportError:
                self.flags = None

            self.SCOPES = data_file["permission-scope"]
            self.APPLICATION_NAME = data_file["application-name"]
            self.EMAIL_ADDRESS = data_file["email"]
            self.EMAIL_ADDRESS_NAME = data_file["email-name"].encode("ascii", "ignore").decode("ascii")
            self.EMAIL_ADDRESS_NAME += " <" + self.EMAIL_ADDRESS + ">"

            try:
                credentials = self.__get_credentials()
                http = credentials.authorize(httplib2.Http())
                self.service = discovery.build('gmail', 'v1', http=http)

                info_text = (self.EMAIL_ADDRESS + " successfully connected to Google Account Gmail API "
                             "over the SimplifiedGmailApi with the following scope: " + self.SCOPES)
                print(info_text)
                logging.info(info_text)
            except Exception as e:
                # >> If there are problems end the script
                self.SetupOk = False
                info_text = (self.EMAIL_ADDRESS + " could not be connected to Google Account Gmail API!\nRead the"
                                                  " README.md file to find out what's wrong and check all your files"
                                                  " on correct information!")
                print(info_text)
                logging.warning(info_text)

            # After this ran you should be logged in and can use the API (if the scope says send)

    """
    Handy and easy to use methods to send plain text or HTML emails with or without attachments:
    """

    def send_plain(self,
                   receiver_email_address,
                   subject="No subject", text="No text."):
        """Send a simple plain (only) text email to someone.

        Args:
        receiver: The email address of the receiver.
        subject: The title of the email.
        text: The text content to be sent to the receiver.

        Returns:
        True if email was sent. False if not.
        """
        return self.__send_mail(receiver_email_address, subject, text)

    def send_plain_with_attachment(self,
                                   receiver_email_address,
                                   subject="No subject", text="No text.",
                                   file_path=None):
        """Send a plain (only) text email to someone with one file attached.

        Args:
        receiver_email_address: The email address of the receiver.
        subject: The title of the email.
        text: The text content to be sent to the receiver.
        file_path: Path to the file that should be attached.

        Returns:
        True if email was sent. False if not.
        """
        return self.__send_mail(receiver_email_address, subject, text, False, file_path)

    def send_plain_with_attachments(self,
                                    receiver_email_address,
                                    subject="No subject", text="No text.",
                                    file_paths=None):
        """Send a plain (only) text email to someone with more than one file attached.

        Args:
        receiver_email_address: The email address of the receiver.
        subject: The title of the email.
        text: The text content to be sent to the receiver.
        file_paths: List of the paths to the files that should be attached.

        Returns:
        True if email was sent. False if not.
        """
        return self.__send_mail(receiver_email_address, subject, text, False, file_paths, True)

    def send_html(self,
                  receiver_email_address,
                  subject="No subject", text="No text."):
        """Send a simple HTML text email to someone.

        Args:
        receiver: The email address of the receiver.
        subject: The title of the email.
        text: The text content to be sent to the receiver.
              ("\n" will automatically be converted to "<br>")

        Returns:
        True if email was sent. False if not.
        """
        return self.__send_mail(receiver_email_address, subject, text, True)

    def send_html_with_attachment(self,
                                  receiver_email_address,
                                  subject="No subject", text="No text.",
                                  file_path=None):
        """Send a HTML text email to someone with one file attached.

        Args:
        receiver_email_address: The email address of the receiver.
        subject: The title of the email.
        text: The text content to be sent to the receiver.
              ("\n" will automatically be converted to "<br>")
        file: Path to the file that should be attached.

        Returns:
        True if email was sent. False if not.
        """
        return self.__send_mail(receiver_email_address, subject, text, True, file_path)

    def send_html_with_attachments(self,
                                   receiver_email_address,
                                   subject="No subject", text="No text.",
                                   file_paths=None):
        """Send a HTML text email to someone with more than one file attached.

        Args:
        receiver_email_address: The email address of the receiver.
        subject: The title of the email.
        text: The text content to be sent to the receiver.
              ("\n" will automatically be converted to "<br>")
        file_paths: List of the paths to the files that should be attached.

        Returns:
        True if email was sent. False if not.
        """
        return self.__send_mail(receiver_email_address, subject, text, True, file_paths, True)

    def send_mail_diy(self,
                      receiver_email_address,
                      subject="No subject", text="No text.",
                      content_is_html=False, file_paths=None):
        """Send an email. Combine the parameter how you like.

        Args:
        receiver_email_address: The email address of the receiver.
        subject: The title of the email.
        text: The text content to be sent to the receiver.
              ("\n" will automatically be converted to "<br>" if the next parameter is True)
        content_is_html: Set true if text is HTML, if it's plain text set it false.
        file_paths: List of the paths to the files that should be attached.

        Returns:
        True if email was sent. False if not.
        """
        return self.__send_mail(receiver_email_address, subject, text, content_is_html, file_paths, True)

    """
    Main send method:
    """

    def __send_mail(self,
                    receiver,
                    subject="No subject", text="No text.", html_mail=False,
                    attachment=None, list_of_attachments=False):
        """Creates an message and sends it.

        Args:
        receiver: The email address of the receiver.
        subject: The title of the email.
        text: The text content to be sent to the receiver.
              ("\n" will automatically be converted to "<br>" if the next parameter is True)
        content_is_html: Set true if text is HTML, if it's plain text set it false.
        file_paths: List of the paths to the files that should be attached.

        Returns:
        True if email was sent. False if not.
        """

        # Check if a receiver email address was entered:
        if receiver is None:
            # >> else abort the process
            self.SetupOk = False
            info_text = "SimplifiedGmailApi could not send email because of missing receiver!"
            print(info_text)
            logging.warning(info_text)

        # Check if all parameter fulfill the minimum conditions (there are strings for them)
        if self.SetupOk:

            # remove bad symbols from text when using python 2
            if self.PYTHON_2:
                subject = subject.replace("ö", "oe").replace("Ö", "Oe").replace("ä", "ae")\
                    .replace("Ä", "Ae").replace("ü", "ue").replace("Ü", "Ue")
                subject = subject.decode("utf-8").encode("ascii", "ignore")

            # Console feedback of message:
            print("Send email from " + self.EMAIL_ADDRESS_NAME + " to: " + receiver + ":")
            print("          " + subject + " (" + ("html" if html_mail else "plain text") + ")")

            if html_mail:
                text = "<br>".join(text.split("\n"))
                output_text = text.split('\n')
            else:
                if self.PYTHON_2:
                    text = text.replace("ö", "oe").replace("Ö", "Oe").replace("ä", "ae")\
                        .replace("Ä", "Ae").replace("ü", "ue").replace("Ü", "Ue")
                    # This will result in data loss because of ascii email
                    text = text.decode("utf-8").encode("ascii", "ignore")

                output_text = text.split('\n')

            i = 1
            for x in output_text:
                print("     " + "{0:04}".format(i) + " " + x)
                i += 1

            if attachment is not None:
                print("          Attachments:")
                print("          " + str(attachment))

            # Create the message:
            # >> check if the text is plain text or HTML
            if html_mail:
                # >> check if there is even an attachment
                if attachment is None:
                    message = self.__create_message(receiver, subject, text, True)
                else:
                    # if it is not python 3 we can continue
                    if self.PYTHON_2:
                        # >> if there is a list list_of_attachments is true
                        message = self.__create_message_with_attachment(receiver, subject, text, True,
                                                                        attachment, list_of_attachments)
                    else:
                        info_text = "This API only supports attachments on python 2.*"
                        print(info_text)
                        logging.warning(info_text)
                        message = None
            else:
                # >> check if there is even an attachment
                if attachment is None:
                    message = self.__create_message(receiver, subject, text)
                else:
                    # if it is not python 3 we can continue
                    if self.PYTHON_2:
                        # >> if there is a list list_of_attachments is true
                        message = self.__create_message_with_attachment(receiver, subject, text, False,
                                                                        attachment, list_of_attachments)
                    else:
                        info_text = "This API only supports attachments on python 2.*"
                        print(info_text)
                        logging.warning(info_text)
                        message = None

            # Send the message:
            # >> check if the Gmail API says the message was sent
            if message is not None and self.__send_message(message) is not None:
                info_text = "Message was successfully send to " + receiver
                print(info_text)
                logging.info(info_text)
                return True
            else:
                info_text = "Message could not be send to " + receiver
                print(info_text)
                logging.warning(info_text)
                return False

        else:
            # >> else abort the process
            info_text = "Something went wrong in the setup! Service stopped. Please check your data."
            print(info_text)
            logging.warning(info_text)
            return False

    """
    Gmail API "unchanged" methods:
    - https://developers.google.com/gmail/api/quickstart/python
    - https://developers.google.com/gmail/api/guides/sending
    """

    def __send_message(self, message):
        """Send an email message.

        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

        Returns:
        Sent Message.
        """
        try:
            message = (self.service.users().messages().send(userId="me", body=message).execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def __create_message(self, to, subject, message_text, message_html=False):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

        Returns:
        An object containing a base64url encoded email object.
        """
        # message_text.encode('us-ascii', 'ignore').decode('us-ascii', 'ignore')

        if message_html:
            message = MIMEText(message_text, 'html')
        else:
            message = MIMEText(message_text)

        message['to'] = to
        message['from'] = self.EMAIL_ADDRESS_NAME
        message['subject'] = subject

        if self.PYTHON_2:
            # PYTHON_2 Pi 3 - Python 2.7.9
            return {'raw': base64.urlsafe_b64encode(message.as_string())}
        else:
            # Windows 10 Pycharm EDU:
            raw = base64.urlsafe_b64encode(message.as_bytes())
            raw = raw.decode()
            body = {'raw': raw}
            return body

    def __get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        credential_dir = self.DIRECTORY_FOR_GMAIL_API
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'gmail_api_.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.PATH_FOR_GMAIL_CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def __create_message_with_attachment(self,
                                         to, subject, message_text, message_html,
                                         file, attachment_list=False):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file: The path to the file to be attached.

        Returns:
        An object containing a base64url encoded email object.
        """
        message = MIMEMultipart()

        message['to'] = to
        message['from'] = self.EMAIL_ADDRESS_NAME
        message['subject'] = subject.encode('ascii', 'ignore')

        if message_html:
            msg = MIMEText(message_text, 'html')
        else:
            msg = MIMEText(message_text)
        message.attach(msg)

        if attachment_list:
            list_of_attachments = file
        else:
            list_of_attachments = [file]

        for attachment in list_of_attachments:
            content_type, encoding = mimetypes.guess_type(attachment)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            if main_type == 'text':
                fp = open(attachment, 'rb')
                msg = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(attachment, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(attachment, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(attachment, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()
            filename = os.path.basename(attachment)
            msg.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(msg)

        if self.PYTHON_2:
            # PYTHON_2 Pi 3 - Python 2.7.9
            return {'raw': base64.urlsafe_b64encode(message.as_string())}
        else:
            # Windows 10 Pycharm EDU:
            raw = base64.urlsafe_b64encode(message.as_bytes())
            raw = raw.decode()
            body = {'raw': raw}
            return body

    if __name__ == "__main__":
        print("Run the demo.py script for a demo or visit"
              " https://github.com/AnonymerNiklasistanonym/SendGmailSimplified. This is a library.")
    else:
        print("SimplifiedGmailApi imported.")
