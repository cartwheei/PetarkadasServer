from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_cors import CORS
import os

from ma import ma
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.confirmation import Confirmation, ConfirmationByUser

app = Flask(__name__)
CORS(app, supports_credentials=True)

# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#     "DATABASE_URL", "DATABASE_URI")  # get metodu iki parametre alır ilki yoksa ikinci parametre defaulttur
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:e83xsf09@localhost/petarkadas'

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = os.environ.get("API_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = "alper2"
api = Api(app)

jwt = JWTManager(app)  # not creating /auth endpoint


@app.before_first_request
def create_tables():
    db.create_all()


# error handleri bircok error için kullanıp daha iyi bir kod yazabiliriz
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):  # except validation error as err
    return jsonify(err.messages), 400


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<string:name>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    ma.init_app(app)
    app.run('0.0.0.0')
    # app.run(port=5000, debug=True)
