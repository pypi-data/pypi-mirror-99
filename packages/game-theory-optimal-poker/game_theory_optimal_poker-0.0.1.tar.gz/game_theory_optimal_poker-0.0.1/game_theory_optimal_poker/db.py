import sqlite3

from flask import current_app, g


def get_db():
    # connects to the database
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows as a dictionary mapping column names to values instead of just a tuple
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    # closes the connection to the database when app exits
    app.teardown_appcontext(close_db)
