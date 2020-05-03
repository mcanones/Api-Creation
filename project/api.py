from flask import Flask, request, jsonify
from settings.settings import PORT
from src.mongo import *
from errors.handlers import *
from bson.json_util import dumps
from errors.handlers import *

app = Flask(__name__)

@app.route("/user/create/<username>")
def insertUser(username):
    id_str = insertUserMongo(username)
    return jsonify({"Result": f"Inserted {username} - ID: {id_str}"})

@app.route("/chat/create")
@errorHandler
def insertChat():
    users_ids = request.args.get("users_ids").split(',')
    chat_id = insertChatMongo(users_ids)
    if chat_id != None:
        return jsonify({"result":"You have created a chat", 
        'Chat ID':chat_id,
        'Members':len(users_ids)})
    return jsonify({"Result":"You are trying to create a chat with users that are not in de DB"})

@app.route("/chat/<chat_id>/adduser")
@errorHandler
def insertMemberInChat(chat_id):
    user_id = request.args.get("user_id")
    members = insertMemberInChatMongo(chat_id, user_id)
    return jsonify({"Result":"You have introduced a user", 
        'In Chat': chat_id,
        'User ID': user_id})

@app.route("/chat/<chat_id>/addmessage", methods=['POST'])
@errorHandler
def insertMessageInChat(chat_id):
    user_id = request.form.get('user_id')
    text = request.form.get('text')
    inserted, msg_str, name = insertMessageInChatMongo(chat_id, user_id, text)
    if inserted:
        return jsonify({"Result": "You have inserted a message",
            "With ID": msg_str,
            "In Chat":chat_id,
            "From User": user_id,
            "Name User": name,
            "Content": text,
            "Date": str(datetime.datetime.now())})
    return jsonify({"Result":"The user_id is not in the chat"})

@app.route("/chat/<chat_id>/list")
def listMessagesChat(chat_id):
    msgs_array = listMessagesChatMongo(chat_id)
    return jsonify({"Result": list(msgs_array)}) 

@app.route("/chat/<chat_id>/sentiment")
@errorHandler
def chatSentiments(chat_id):
    msgs, avg_scores = chatSentimentsMongo(chat_id)
    return jsonify({'Average Score Chat': {'Negative':avg_scores[0], 'Neutral':avg_scores[1], 'Positive':avg_scores[2] }, 'Messages': msgs})

@app.route("/user/<user_id>/recommend")
@errorHandler
def recommendUsers(user_id):
    recommendations = recommendUsersMongo(user_id)
    return jsonify({'Result': recommendations})

app.run("0.0.0.0", PORT, debug=True)

