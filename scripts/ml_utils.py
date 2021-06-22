import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json
import dill


def clean_date(data):
    return pd.to_datetime(data['upload_date'], format='%Y-%m-%d')


def clean_views(data):
    return data['view_count'].map(lambda x: 0 if x<0 else int(x))
    # return 0 if data['view_count']<0 else int(data['view_count'])



def compute_features(data):
    # print('**************************************')
    # print(data)

    publish_date = clean_date(data)
    if publish_date is None:
        return None
    # print(data)

    views = clean_views(data)
    title = data['title']

    features = pd.DataFrame(index=data.index)

    features['tempo_desde_pub'] = (pd.Timestamp.today() - publish_date) / np.timedelta64(1, 'D')
    features['views'] = views
    features['views_por_dia'] = features['views'] / features['tempo_desde_pub']
    del features['tempo_desde_pub']

    title_vec = jb.load("modelos/title_vectorizer_20200208.pkl.z")

    vectorized_title = title_vec.transform(title)

    # num_features = csr_matrix([features['views'], features['views_por_dia']])   
    feature_array = hstack([features, vectorized_title])
    # print(feature_array)
    return feature_array


def compute_prediction(data):
    feature_array = compute_features(data)

    if feature_array is None:
        return 0

    with open('modelos/logistic_reg_20200208.pkl.z', 'rb') as file:
        model_lr = dill.load(file)

    #p_lr = jb.load("modelos/logistic_reg_20200208.pkl.z")
    mdl_lgbm = jb.load("modelos/lgbm_20200208.pkl.z")
    
    # print('88888888888888')
    # print(model_lr.predict_proba(csr_matrix(feature_array)))

    p_lr = model_lr.predict_proba(csr_matrix(feature_array))[:,1]
    p_lgbm = mdl_lgbm.predict_proba(feature_array)[:, 1]

    p = 0.7*p_lr+0.3*p_lgbm
    #log_data(data, feature_array, p)

    return p

def log_data(data, feature_array, p):

    #print(data)
    video_id = data.get('og:video:url', '')
    data['prediction'] = p
    data['feature_array'] = feature_array.todense().tolist()
    #print(video_id, json.dumps(data))







