import pandas as pd
import youtube_dl
import numpy as np

def get_data_video(query, ydl):
    #ydl = youtube_dlc.YoutubeDL({"ignoreerrors": True})
    resultados = []
    
    r = ydl.extract_info("ytsearchdate10:{}".format(query), download=False)
    for entry in r['entries']:
        if entry is not None:
            entry['query'] = query
    resultados += r['entries']
    resultados = [e for e in resultados if e is not None]

    df = pd.DataFrame(resultados)

    # print(df)
    df_filtrado = df[['id','webpage_url','title','playlist','view_count','like_count','dislike_count','average_rating',
                        'description','categories','tags','upload_date','channel_url', 'thumbnail','width','height','resolution','fps']] #'subscriber_count'
    df_filtrado.loc[:, 'id'] = 'watch?v='+df_filtrado.loc[:, 'id']
    df_filtrado.rename(columns={'id':'link','playlist':'query'}, inplace=True)
    # print(df_filtrado)
    return df_filtrado

def get_data_one_video(link):
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True}) 
    
    r = ydl.extract_info(link, download=False)
    cols =['id','webpage_url','title','playlist','view_count','like_count','dislike_count','average_rating',
                        'description','categories','tags','upload_date','channel_url', 'thumbnail','width','height','resolution','fps']

    # print(len(r))
    # print(r.keys())
    # print([r.get(x) for x in cols])
    # input()
    df = pd.DataFrame(columns=cols)
    df.loc[0,:] = [r[x] for x in cols]

    # print(df)
    df_filtrado = df[cols] #'subscriber_count'
    df_filtrado.loc[:, 'id'] = 'watch?v='+df_filtrado.loc[:, 'id']
    df_filtrado.rename(columns={'id':'link','playlist':'query'}, inplace=True)
    # print(df_filtrado)
    return df_filtrado
