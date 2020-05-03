import sys
sys.path.append("..") 
from pymongo import MongoClient
from project.settings import DBURL
from pymongo import ReturnDocument
from bson import ObjectId
from src.getRecommendations import getRecommendations
from src.getScoreSentiment import getScoreSentiment
import datetime
from errors.handlers import *

#Download DB and Collections

client = MongoClient(DBURL, maxPoolSize=50, connect=False)
db = client["Project"]
messages = db["Messages"]
chats = db["Chats"]
users = db["Users"]

#Functions interacting with MongoDB

def insertUserMongo(username):
    data = { "name": f"{username}"}
    user = users.insert_one(data)
    id_str = str(user.inserted_id)
    return id_str

def insertChatMongo(users_ids):
    tot_users_ob = list(users.find({ },{'_id':1}))
    if not tot_users_ob:
        print("ERROR")
        raise Error404("There are not users in the DB")
    tot_users_str = [str(e['_id']) for e in tot_users_ob]
    if {*users_ids}.issubset({*tot_users_str}):
        data = { "members": users_ids }
        chat = chats.insert_one(data)
        id_chat = str(chat.inserted_id)
        return id_chat
    return None

def insertMemberInChatMongo(chat_id, user_id):
    tot_users_ob = list(users.find({ },{'_id':1}))
    tot_users_str = [str(e['_id']) for e in tot_users_ob]
    members = list(chats.find({'_id': ObjectId(chat_id)},{'_id':0, 'members':1}))
    if not members:
        print("ERROR")
        raise Error404("Chat_id not found")
    members = members[0]['members']
    if user_id in tot_users_str:
        if  user_id not in members:
            chats.update(
            {'_id': ObjectId(chat_id)},
            {'$push': {"members":user_id}})
            return members
        else: 
            raise Error404("User_id is already in the chat")
    else: 
        raise Error404("User_id is not in the DB")
   
def insertMessageInChatMongo(chat_id, user_id, text):
    members = list(chats.find({'_id': ObjectId(chat_id)},{'_id':0, 'members':1}))
    if not members:
        print("ERROR")
        raise Error404("chat_id not found")
    members = members[0]['members']
    name = list(db.Users.find({'_id': ObjectId(user_id)},{'_id':0, 'name':1}))[0]['name']
    if user_id in members:
        scores = getScoreSentiment(text)
        data = { "chat_id": chat_id,
                "user_id": user_id,
                "name": name,
                "message": text,
                "date": datetime.datetime.now(),
                "negative_score": scores['neg'],
                "neutral_score": scores['neu'],
                "positive_score": scores['pos']}
        message = messages.insert_one(data)
        msg_str=str(message.inserted_id)
        return True, msg_str, name
    return False, None, None

def listMessagesChatMongo(chat_id):
    msgs_array = messages.find({'chat_id': chat_id},{'_id':0, 'name':1, 'message':1})
    if len(list(msgs_array))==0:
        print("ERROR")
        raise Error404("chat_id not found")
    return msgs_array

def chatSentimentsMongo(chat_id):
    msgs= list(messages.find({'chat_id': chat_id},{'_id':0, 'name':1,  'message':1, 'negative_score':1, 'neutral_score':1,'positive_score':1 }))
    scores_cat=['negative_score', 'neutral_score', 'positive_score']
    avg_scores=[]
    for e in scores_cat:
        avg_scores.append(sum([m[e] for m in msgs])/len(msgs))
    if not msgs:
        print("ERROR")
        raise Error404("chat_id not found")
    return  msgs, avg_scores

def recommendUsersMongo(user_id):
    recommendations = getRecommendations(user_id, messages)
    if not recommendations:
        print("ERROR")
        raise Error404("user_id not found")
    return recommendations
  



