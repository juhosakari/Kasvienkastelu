from flask import Flask, render_template, url_for
import socket
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models