from PyMessagingFramework.framework import MessagingFramework
from emailme_emailservice.commands.email_command import EmailCommand
from emailme_emailservice.handlers.email_handler import EmailHandler

import os

# Set RabbiMQ credentials and the EmailService Queue name
MQ_HOST = os.getenv('MQ_HOST', 'rabbitmq')
MQ_PORT = int(os.getenv('MQ_PORT', '5672'))
MQ_USERNAME = os.getenv('MQ_USERNAME', 'guest')
MQ_PASSWORD = os.getenv('MQ_PASSWORD', 'guest')
QUEUE_NAME = os.getenv('EMAILME_EMAILSERVICE_QUEUE', 'emailme_emailservice')


if __name__ == "__main__":
    # Instantiate the messaging framework
    framework = MessagingFramework(
        broker_url=MQ_HOST, # URL of rabbiMQ
        broker_port=MQ_PORT, # port of rabbiMQ
        broker_username=MQ_USERNAME, # username of rabbiMQ
        broker_password=MQ_PASSWORD, # password of rabbiMQ
        queue_name=QUEUE_NAME, # Queue name of consumer,
        auto_delete=True, # Whether to auto delete the queue when application is stopped
        non_blocking_connection=False # Creates a non blocking connection
    )

     # Register the command with the QUEUE to which it should be forwarded
    framework.register_commands_as_consumer(command=EmailCommand, handler=EmailHandler)

    # It connects to the message broker and creates required queue and then starts listening for messages
    print("Starting application")
    framework.start()
