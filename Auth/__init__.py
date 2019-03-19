from flask import Flask

from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*", "Access-Control-Allow-Headers": "Content-Type,Authorization,iduser,token"}})