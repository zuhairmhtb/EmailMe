from PyMessagingFramework.framework import BaseCommandHandler
from emailme_emailservice.commands.email_command import EmailCommand

class EmailHandler(BaseCommandHandler):

    def handle(self, command:EmailCommand):
        print(f"Sending email to {command.recipient}\nSubject:{command.subject}\nBody:{command.body}")