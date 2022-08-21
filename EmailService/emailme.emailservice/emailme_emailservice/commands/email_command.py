from PyMessagingFramework.framework import BaseCommand
from typing import List

class EmailCommand(BaseCommand):

    def __init__(self, body:str, subject:str, recipient:str):
        self.body = body
        self.subject = subject
        self.recipient = recipient