# EmailMe (WebService)

This application is a web service developed using Django. The application will receive a text body, subject and a recipient email address as input. It will then forward the content to EmailService which will then send the email to the recipient.

The application uses RabbitMQ as the message broker and PyMessagingFramework as the wrapper around the message broker to communicate with other microservices.

We will use poetry as package manager as it has the ability to manage public and private packages. We will install command list as private packages of other microservices. We will use PyMessagingFramework to forward the command to respective microservices.


## Process of communication

1. User navigates to homepage and provides email subject, body and recipient.

2. The data is passed to view.

3. View creates a command object and forwards the command to PyMessagingFramework.

4. PyMessagingFramework parses the command and forwards it to RabbitMQ.

5. RabbitMQ forwards the command to PyMessagingFramework of EmailService.

6. PyMessagingFramework decodes the command and calls the appropriate handler.

7. The handler sends an email to the recipient.