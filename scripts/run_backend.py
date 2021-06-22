from get_data import *
from ml_utils import *
import time
import youtube_dl
import os
import sqlite3 as sql 


queries = ["data+science","ciencia+de+dados", "machine+learning", "aprendizado+de+maquina", "kaggle"]#["machine+learning", "data+science", "kaggle"]

def update_db():
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True})#

    with open("novos_videos.json", 'w+') as output:
        for query in queries:
                print(query)
                try:
                    data = get_data_video(query, ydl)
                except Exception as e:
                    print(e) 
                    #os.remove("novos_videos.json")
                    continue

                
                p = compute_prediction(data)

                video_id = 'https://www.youtube.com/'+data['link']#.values.tolist()
                data_front = {"title": data['title'], "score": p, "video_id": video_id}
                data_front['update_time'] = time.time_ns()
                # print(data_front)
                for idx, data_row in pd.DataFrame(data_front).iterrows():
                    print(video_id, json.dumps(data_row.to_dict()))
                    output.write("{}\n".format(json.dumps(data_row.to_dict())))
    return True

db_name = 'videos.db'

def update_db_sqlite():
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True})#
    
    with sql.connect(db_name) as conn:
        for query in queries:
                print(query)
                try:
                    data = get_data_video(query, ydl)
                except Exception as e:
                    print(e) 
                    #os.remove("novos_videos.json")
                    continue
                
                p = compute_prediction(data)

                video_id = 'https://www.youtube.com/'+data['link']#.values.tolist()
                data_front = {"title": data['title'],  "video_id": video_id, "score": p}
                data_front['update_time'] = time.time_ns()
                # print(data_front)
                for idx, data_row in pd.DataFrame(data_front).iterrows():
                    # print(video_id, json.dumps(data_row.to_dict()))
                    # print({**data_row.to_dict()})
                    c = conn.cursor() #
                    print('INSERT INTO videos VALUES ("{title}", "{video_id}", {score}, {update_time})'.format(**data_row.to_dict()))
                    c.execute('INSERT INTO videos VALUES ("{title}", "{video_id}", {score}, {update_time})'.format(**data_row.to_dict())) #
                    conn.commit() #
    return True