"""
Adapted from Flask tutorial - https://flask.palletsprojects.com/en/1.1.x/tutorial/
Uses flask_socketio to create a web socket connection between client and server
with socketIO JavaScript library. 
See official docs - https://flask-socketio.readthedocs.io/en/latest/

Run from command line with:
gunicorn --worker-class eventlet -w 1 'poker:create_app()'
"""
__version__ = "0.0.1"
from flask import Flask
from flask_socketio import SocketIO
from pathlib import Path


socketio = SocketIO(logger=True, engineio_logger=True)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    instance_path = Path(app.instance_path)
    db_location = instance_path / "hand_history.sqlite"
    print('db_location is', db_location)
    app.config.from_mapping(SECRET_KEY="DEV", DATABASE=db_location)

    if not db_location.exists():
        # initialize database if it does not exist
        import sqlite3
        con = sqlite3.connect(db_location)
        with open(instance_path / "schema.sql", 'r') as f:
            sql_string = f.read()
        cur = con.cursor()
        cur.executescript(sql_string)

    # register views
    from . import db, auth, play

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(play.bp)
    app.add_url_rule("/", endpoint="index")

    socketio.init_app(app)
    return app
