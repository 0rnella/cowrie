from flask import Flask
from flask_cors import CORS
from flask.logging import create_logger

# configuration
DEBUG = True

# instantiate app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# create a logger
log = create_logger(app)

# import routes
from app import routes

if __name__ == '__main__':
    app.run()