cd /home/python-websockets-server/

git pull

gunicorn -k flask_sockets.worker -b 0.0.0.0:8000 app:app