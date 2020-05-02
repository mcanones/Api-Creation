import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
from errors.handlers import *

def getRecommendations(user_id, messages):

    #Diccionario de usuarios 
    list_users = list(messages.find({ },{'_id':0, 'user_id':1}))
    list_users = set([e['user_id'] for e in list_users])
    dict_users = dict.fromkeys(list_users, "")
    if user_id not in dict_users:
        print("ERROR")
        raise Error404("user_id not found")
    
    #Rellenar diccionario con los mensajes 
    for us_id, _ in dict_users.items():
        msgs = list(messages.find({'user_id':us_id},{'_id':0, 'message':1}))
        msgs_flat = [e['message'] for e in msgs]
        msgs_str = ' '.join(msgs_flat)
        dict_users[us_id]=msgs_str

    #Montar tabla usuario vs palabras
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(dict_users.values())
    m = sparse_matrix.todense()
    users_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(users_term_matrix, 
                    columns=count_vectorizer.get_feature_names(), 
                    index=dict_users.keys())

    #Montar tabla distancias
    similarity_matrix = distance(df,df)
    sim_df = pd.DataFrame(similarity_matrix, columns=dict_users.keys(), index=dict_users.keys()) 

    #Obtener las recommendations
    rec_user_id = sim_df[user_id].sort_values(ascending=False)[1:4]
    rec=list(zip(rec_user_id.index,rec_user_id))

    return rec