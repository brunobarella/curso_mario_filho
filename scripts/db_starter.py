import run_backend
import sqlite3 as sql
import time
import os


if __name__ == "__main__":
    novos_videos_db = "videos.db"
    if os.path.isfile(novos_videos_db):
        last_update = os.path.getmtime(novos_videos_db) * 1e9
    else:
        last_update = 2592000000000000 + time.time_ns() + 1

    if time.time_ns() - last_update > (720*3600*1e9) or not os.path.isfile(novos_videos_db): # aprox. 1 mes
        if os.path.isfile(novos_videos_db):
            os.remove(novos_videos_db)
        with sql.connect(run_backend.db_name) as conn:
            c = conn.cursor()
            # Create table
            c.execute('''CREATE TABLE videos
                        (title text, video_id text, score real, update_time integer)''')
            conn.commit()
        run_backend.update_db_sqlite()