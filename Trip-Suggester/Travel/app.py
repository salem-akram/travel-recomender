from flask import Flask
from config import Config
from models import db
from routes import register_routes
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)


db.init_app(app)
register_routes(app)


if __name__ == '__main__':
    app.run(debug=True, port=5001)