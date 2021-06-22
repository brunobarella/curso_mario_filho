FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++ 
RUN pip install -r requirements.txt
RUN python db_starter.py
#CMD python ./app.py

# Run the image as a non-root user
# RUN adduser -D myuser
# USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi 
# CMD gunicorn --bind 0.0.0.0:80 wsgi 

# contruir o docker localmente
# docker build . -t youtube
# rodar o docker local
# docker run -e PORT=80 -p 80:80 youtube

#https://github.com/microsoft/LightGBM/blob/master/docker/dockerfile-python
#https://github.com/heroku/alpinehelloworld
#https://devcenter.heroku.com/articles/container-registry-and-runtime

#Creating app... done, ⬢ fast-cove-83969

#https://fast-cove-83969.herokuapp.com/ | https://git.heroku.com/fast-cove-83969.git


#https://sheltered-reef-65520.herokuapp.com/ | https://git.heroku.com/sheltered-reef-65520.git

# passo a passo pra mandar pra la:

#heroku container:login

# mandando para o heroku
# heroku container:push web -a fast-cove-83969

# ativando o docker no heroku
# heroku container:release web -a fast-cove-83969
