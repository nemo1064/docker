# Docker

Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package.

## Description

Dockerising two simple REST-APIs -
    1. Counts the number of visitors and performs simple operations suchs as "Addition","Subtraction", "Multiplication" and "Division" on two numbers received via POST method.

    2.Provides database as a service to store sentences.
      Supports-
        User registrations.
        Storing the sentence.
        Token based spending (i.e for each opearation performed a token is deducted).


## Usage

```
Goto the Docker directory

Goto db_api or counting_api directory 

Run the following commands:

sudo docker-compose build
sudo docker-compose up

```
