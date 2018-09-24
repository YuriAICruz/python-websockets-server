#! /bin/sh

cd /var/python-websockets-server/

git checkout .
git pull

pip install -r requirements.txt

gunicorn -k flask_sockets.worker -b 0.0.0.0:8000 app:app

exec "$@"
