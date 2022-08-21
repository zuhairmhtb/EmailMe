from PyMessagingFramework.framework import BaseCommand
from typing import List

class EmailCommand(BaseCommand):
    """
    This is the command which is sent to the Email handler. It is sent by the producer to the 
    consumer in order make the consumer perform some task.
    """

    def __init__(self, body:str, subject:str, recipient:str):
        """
        @param body: A string containing the email body
        @param subject: A string containing the email subject
        @param recipient: A string containing the recipient's email address
        """
        self.body = body
        self.subject = subject
        self.recipient = recipient