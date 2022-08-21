# EmailMe - A Pythonic Microservice Architecture

[Microservice architecture](https://en.wikipedia.org/wiki/Microservices) is one of the software system architectures which is commonly used to build scalable complex systems. I have recently been looking into different ways I can create a scalable microservice architecture with Python. [Django](https://www.djangoproject.com/) is a python based web framework that I have been using for a long time to develop [monolithic](https://en.wikipedia.org/wiki/Monolithic_application) applications. 

With the emergence of technologies like [Docker](https://www.docker.com/), [Kubernetes](https://kubernetes.io/), [message brokers](https://en.wikipedia.org/wiki/Message_broker), etc. it is now feasible, affordable and possible to develop well designed microservice architectures in relatively short amount of time. 

I have been used to developing microservice applications using .Net Framework, especially since it has a large eosystem and community. Technologies like [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/), [Nuget](https://www.nuget.org/), [NServiceBus](https://particular.net/nservicebus) enables us to develop microservices and effectively integrate [CI/CD](https://en.wikipedia.org/wiki/CI/CD) pipeline with it. 

## Sharing codebase

One of the challenges that I faced when developing a microservice application using Python is the management of private and public packages. When developing any application we largely use public packages from the [PyPi](https://pypi.org/) repository. However, when developing a microservice application we need to share certain codebase with multiple applications. Creating private python packages makes the task of sharing codebase easy. Furthermore, when we update the private package it becomes easier to update the version in all the applications using the package.

When developing an application it is easy to install packages with [pip](https://pypi.org/project/pip/) from multiple repositories using the following command:

```
python -m pip install --index-url <repository url> <package name>
```

But when implementing a CI/CD pipeline we normally do not install each package individually. Rather we prefer generating a file like requirements.txt which contains all the packages that needs to be installed. We then use the package manaeger to install all the packages from the generated file. One issue that I faced is, requirements.txt contains just the package name and version. It does not contain the repository url. It is true that we can pass private repository names via '--extra-index-url' parameter. But it contains a security issue. If someone creates a malicious package using the same name as that of our private packages, provide higher version number and upload the package to PyPI, our application will attempt to download the malicious package from the public repository instead of using our private repository for it. 

One approach to solving the problem is to pull all the public packages used in our application to the private repository and then install all packages from private repository thereby, disabling installation from PyPi. But managing all public packages in a private repo, maintaining the packages and adding new packages to the private repo when a developer adds a public package to an application is quite cumbersome.

So, I started looking into different package managers for python that might provide me the ability to manage private and public packages easily and provide me the option to securely pull packages from multiple repositories, especially when pulling the packages automatically in the CI/CD pipeline. Then I came across [Poetry](https://python-poetry.org/) which is a tool for dependency management and packaging in python. It contains a 'pyproject.toml' file and 'poetry.lock' file which helps us install the packages securely.


## Inter-service communication

The other challenge which I faced was integrating the mechanism for communication between the different microservices in our application. There are a lot of ways to achieve this goal. We can use HTTP protocol to communicate with other applications via HTTP requests. In that case, we will need to manually construct the mechanism to securely communicate between the services. Another modern approach is to use a message broker which acts as a communication medium between the services. [RabbitMQ](https://www.rabbitmq.com/) is a state-of-the-art message broker which enables this feature. Moreover, python contains a lot of packages like [Pika](https://pika.readthedocs.io/en/stable/) which helps the integration of RabbitMQ with python applications. However, one of the standard ways to pass messages via message broker is through [JSON](https://www.w3schools.com/js/js_json_intro.asp) objects. There are mainly two types of messages that are passed from one service to another: Commands and Events. Let us take a look at the command based communication:

**Service A** is a [producer](https://www.oreilly.com/library/view/building-event-driven-microservices/9781492057888/ch10.html) which will send a **command** to **Service B** which will act as the [consumer](https://www.oreilly.com/library/view/building-event-driven-microservices/9781492057888/ch10.html). The **command** contains a message and a ID. The message is a string and the ID is an integer.

1. First we will create the command as a JSON object inside **Service A** as follows:

```
{
    "ID": 1,
    "message": "Hello world"
}
```

2. We will then pass the command to a [message queue](https://aws.amazon.com/message-queue/) of the message broker. We will choose the queue to which the consumer is listening.

3. The message broker will then forward the command to **Service B** (consumer).

4. **Service B** will then take the message and call a method which is associated for the command. It will pass the message as input to the method and the method will perform some task.


In the above scenario we have a problem. Suppose we have 50 producers, each of which is a different service and those services can send the same **command** to the consumer. Now suppose at some point in time we want to add a new paramter **author** to the command. To add this new parameter we have to go through all the producer applications, search all the files to seek out where we send the JSON command. Then add the new parameter to all the JSON commands. This process can be quite annoying. We can create a system where all the commands go through a central point but we need to do this for all the services.

What if all our commands resided in the consumer application as independent classes along with the handlers (methods which performs the task when a command is sent to the consumer)? In that case, when we add a new parameter to the handler, we can add the same parameter to the command class. We can share the list of commands availbale for the consumer as a private python package. All other services which needs to communicate with the consumer can install the command package and use the package to create objects from the command classes and then pass the object to the consumer itself. It can make the management of the commands and the handlers very smooth. When we add a new parameter to the command we can simply update the package of all producers and they will then have the updated command class.

[PyMessagingFramework](https://pypi.org/project/PyMessagingFramework/) is a messaging framwork which sits between a service and the message broker. All we need to do is attach command classes to its corresponding handler methods for a consumer and attach command classes to its corresponding message queues for producers. We can then pass the command object from producer to the messageing framework. PyMessagingFramework will then convert the object to appropriate format that the message broker understands. It will then route the message to the appropriate queue. On the other side, inside the consumer - it will receive the message convert it back to the command object and pass the object to its corresponding handler. One advantage with this package is that we can play with python objects instead of JSON objects. On the other hand, PyMessagingFramework decouples the message broker from the services. A service should not care which message broker is being used. If we change the message broker we should not have to update the code structure in our application.

## Architecture

After solving both the above problems, the microservice architecture which I designed is as follows:

<img src="system_architecture.png" alt="system_architecture" style="width: 100%; height: auto; display: block; clear: both: margin: 10px; background-color: #fff;">

We first create the consumer (Service A) and create the command classes in a separate folder called **commands**. We then publish the **commands** package to our private repository. We then connect the consumer to the PyMessagingFramework and connect PyMessagingFramework to the Message Broker.

Next we create the producer (Service B) and install the command package inside the producer via poetry. Then we attach the message queue of consumer (QUEUE Service A) with each command of the command package through PyMessagingFramework. Then we connect PyMessagingFramework to the Message Broker.

We can then easily publish a command from Service B to Service A.


## Task

The microservice application which we will be creating contains two services:

1. WebService: This application is web application developed using Django. Users can send emails through this application. They can provide an email subject, email body and a recipient's email address. When they submit the form, the application will forward this data as a command to the consumer.

2. EmailService: This application is a microservice application developed using PyMessagingFramework. This service receives the email contents from WebService and then prints it out in the console.

We containerized the entire system using docker so that anyone can clone the project and easily start the system using the docker-compose file.

In this tutorial, we will go through the major portion of each important file to see what each section does and how the entire system interacts with each other.

The tutorial contains the following pre-requisites:

1. Python

2. [Docker](https://www.docker.com/)

3. [RabbitMQ](https://www.rabbitmq.com/)

4. [Poetry](https://python-poetry.org/)

5. [Microservice architecture](https://en.wikipedia.org/wiki/Microservices)

6. [Django](https://www.djangoproject.com/)

7. [PyPi](https://pypi.org/)

A basic understanding of these technologies will be very helpful to follow along with me.

I have used the following technologies in the application:

1. [Docker](https://www.docker.com/)

2. [RabbitMQ](https://www.rabbitmq.com/)

3. Private PyPi Server

4. [PyMessagingFramework](https://pypi.org/project/PyMessagingFramework/)

5. [Django](https://www.djangoproject.com/)