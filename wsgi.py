import eventlet
from eventlet import wsgi
from app import app

wsgi.server(eventlet.listen(("0.0.0.0", 5001)), app)
