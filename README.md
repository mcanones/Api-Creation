# Api-Creation

<p align="center">
 <img src="./images/api.png"/>
</p>

## Scope:

The aim of this project is to create an api of chat messages, to later analyze the conversations. Functionalities:

- ✅ Store chat messages in a cloud database 
- ✅ Extract sentiments from chat messages 
- ✅ Recommend friends to a user based on chat contents using a recommender system with `NLP` analysis 
- ✅ The service is deployed with Docker to Heroku 

**Docker** is a tool designed to make it easier to create, deploy, and run applications by using containers. A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another. 

**Heroku** is a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

## Do you want to try the API? 

🔥`MIRIAPI`🔥 is the web application used to launch the API 🚀. You can interact with it in the following way:

Basic path: `https://miriapi.herokuapp.com` (You should add some of the following terminations)

**SCHEMA**: `PATH` + `TERMINATIONS` 

1) (GET) Welcome message: **/**
2) (GET) Introduce users in the database: **/chat/create/`<name>`**
3) (GET) Create a chat with users: **/chat/create** -> **params**=[`<user_id>`, `<user_id>`,...]
4) (GET) Add user in a pre-existing chat: **/chat/`<chat_id>`/adduser** -> **params**={"user_id":`<user_id>`}
5) (POST) Add a message: **/chat/`<chat_id>`/addmessage** -> **data**={"user_id":`<user_id>`, "chat_id":`<chat_id>`}
6) (GET) Obtain all the messages in a chat: **/chat`<chat_id>`/list**
7) (GET) Get the sentimes score of a specific chat: **/chat`<chat_id>`/sentiment**
8) (GET) Recommend 3 friends to a user depending on chat contents: **/user`<user_id>`/recommend**

Examples of use:

- https://miriapi.herokuapp.com/

- https://miriapi.herokuapp.com/user/create/miriam 

- https://miriapi.herokuapp.com/chat/5eadb94fbbbaa3faa1599730/list 

- https://miriapi.herokuapp.com/chat/5eadb94fbbbaa3faa1599730/sentiment

- https://miriapi.herokuapp.com/user/5eada20b9b27ff529f8d56b5/recommend

## Cloud DB 

- `MongoATLAS`

## Design of the API

- **Flask** 

## Links:

The comments in the database are extracted from **The Witcher** Netflix Serie.

- URL: https://transcripts.fandom.com/wiki/Four_Marks

## Database Schema Implemented:

<p align="center">
 <img src="./images/db.png" width="950" height="550"/>
</p>

