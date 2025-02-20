from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(import_name=__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
database = SQLAlchemy(app)

swaggerui_blueprint = get_swaggerui_blueprint(
    "/docs",
    "/static/swagger.json",
    config={ 
        "app_name": "Demonstration-1"
    }
)
app.register_blueprint(swaggerui_blueprint)


from app import routers