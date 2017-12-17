import os.path
from app import app, socketio


# app = create_app(DB_PATH)
app.host = '127.0.0.1'
app.debug = True


if __name__ == '__main__':
    socketio.run(app)
