# deploy_front/app.py
#

import os.path
from flask import Flask, request, render_template, redirect, flash
import os
import json
import run_backend

import get_data #
import ml_utils #

import sqlite3 as sql  # 
import pandas as pd

import time

app = Flask(__name__)
app.secret_key = "super secret key"

def get_predictions():

    videos = []
    
    novos_videos_json = "novos_videos.json"
    if not os.path.exists(novos_videos_json):
        run_backend.update_db()
    
    last_update = os.path.getmtime(novos_videos_json) * 1e9

    #if time.time_ns() - last_update > (720*3600*1e9): # aprox. 1 mes
    #    run_backend.update_db()

    with open("novos_videos.json", 'r') as data_file:
        for line in data_file:
            line_json = json.loads(line)
            videos.append(line_json)

    predictions = []
    for video in videos:
        #print(video)
        #print(video['video_id'])
        predictions.append((video['video_id'], video['title'], float(video['score'])))

    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]


    predictions_formatted = []
    for e in predictions:
        print(e)
        predictions_formatted.append("<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>".format(title=e[1], link=e[0], score=e[2]))
  
    return '\n'.join(predictions_formatted), last_update

def get_predictions_sql():
    videos = []

    novos_videos_db = "videos.db"
    if not os.path.exists(novos_videos_db):
        run_backend.update_db_sqlite()
    
    last_update = os.path.getmtime(novos_videos_db) * 1e9

    if time.time_ns() - last_update > (720*3600*1e9): # aprox. 1 mes
       run_backend.update_db_sqlite()

    with sql.connect(run_backend.db_name) as conn: # 
        c = conn.cursor() #
        for line in c.execute("SELECT * FROM videos ORDER BY score DESC"): #
            #(title, video_id, score, update_time)
            line_json = {"title": line[0], "video_id": line[1], "score": line[2], "update_time": line[3]} #
            videos.append(line_json)
			

    # predictions = []
    # for video in videos:
    #     predictions.append((video['video_id'], video['title'], float(video['score'])))

    # predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]


    # predictions_formatted = []
    # for e in predictions:
    #     #print(e)
    #     predictions_formatted.append("<tr><th><a href=\"{link}\">{title}</a></th><th>{score}</th></tr>".format(title=e[1], link=e[0], score=e[2]))
  
    # return '\n'.join(predictions_formatted), last_update
    return videos, last_update

@app.route('/delete')
def delete():
    id = request.args['id']
    # print(id)
    try:
        with sql.connect(run_backend.db_name) as conn: # 
            c = conn.cursor() #
            c.execute(f"DELETE FROM videos WHERE video_id='{id}'")
            # c.commit() 
        return redirect('/')
    except:
        return "There was a problem deleting data. "+f"DELETE FROM videos WHERE video_id='{id}'"

@app.route('/predict', methods=['GET',"POST"])
def predict():
    if request.method == 'POST':

        link = request.form['link']
        
        try:
            data = get_data.get_data_one_video(link)
        except Exception as e:
            print(e)
            flash('Erro na predição! ')
            
        try:
            p = ml_utils.compute_prediction(data)
            flash(data.loc[0, 'title'])
            flash(data.loc[0, 'webpage_url'])
            flash(f'Score: {p[0]}')
        except Exception as e:
            print(e)
            flash('Erro')


        return render_template('/prediction.html')
    else:
        return render_template('/prediction.html')

@app.route('/')
def main_page():
    preds, last_update = get_predictions_sql() #get_predictions()
    # videos = pd.DataFrame(preds, columns=['title','video_id', 'score',])
    # videos.sort_values(by='score', inplace=True)
    return render_template('index.html', videos=preds)
    # return """<head><h1>Recomendador de Vídeos do Youtube</h1></head>
    # <body>
    # Segundos desde a última atualização: {}
    # <table>
    #          {}
    # </table>
    # </body>""".format((time.time_ns() - last_update) / 1e9, preds)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')