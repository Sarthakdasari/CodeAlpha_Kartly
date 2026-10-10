import os, sqlite3
from flask import g, current_app
from seed import seed
def connect(path):
    db = sqlite3.connect(path, isolation_level=None)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db
def get_db():
    if "db" not in g: g.db = connect(current_app.config["DATABASE"])
    return g.db
def init_db(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    db = connect(path)
    with open(os.path.join(os.path.dirname(__file__), "schema.sql")) as f: db.executescript(f.read())
    seed(db); db.close()
def init_app(app):
    init_db(app.config["DATABASE"])
    @app.teardown_appcontext
    def close(_):
        db = g.pop("db", None)
        if db: db.close()
