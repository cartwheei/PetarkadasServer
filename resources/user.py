import traceback
from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required,
    create_refresh_token,
    create_access_token,
    jwt_refresh_token_required,
    get_jwt_identity,)


from schemas.user import UserSchema
from models.user import UserModel
from models.confirmation import ConfirmationModel
from libs.strings import gettext

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": gettext("user_username_exists")}, 400

        if UserModel.find_by_email(user.email):
            return {"message": gettext("user_email_exists")}, 400

        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            # user.send_confirmation_email()
            return {"message": gettext("user_registered")}, 201

        except:  # failed to save user to db
            traceback.print_exc()
            user.delete_from_db()
            return {"message": gettext("user_error_creating")}, 500


class User(Resource):
    @classmethod
    def get(cls, name: str):
        user = UserModel.find_by_username(name)
        if user:
            return user_schema.dump(user), 200
        return {"message": gettext("user_not_found")}, 404

    @classmethod
    def delete(cls, name: str):
        user = UserModel.find_by_username(name)
        if user:
            user.delete_from_db()
            return {"message": gettext("user_deleted")}, 200
        return {"message": gettext("user_not_found")}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        json = request.get_json()
        # login yapılırken mail istemeye gerek yok
        user_data = user_schema.load(json, partial=("email",))
        # find use in database
        user = UserModel.find_by_username(user_data.username)
        # check password
        # create acces token
        # create refresh token
        if user and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            confirmation.change_expire_date()
            # if confirmation and confirmation.confirmed:
            # this is what the identity() function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return ({"access_token": access_token, "refresh_token": refresh_token, "user_id": user.id},
                    200)
            # return {"message": gettext("user_not_confirmed").format(user.email)}, 400
        return {"message": gettext("user_invalid_credentials")}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        print(user_id)
        user = UserModel.find_by_id(user_id)
        confirmation = user.most_recent_confirmation
        ConfirmationModel.force_to_expire(confirmation)
        return {"message": gettext("user_logged_out").format(user.username)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200


class UserLoginToken(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        confirmation = user.most_recent_confirmation
        if user and confirmation:
            if confirmation.expired:
                return ({"message": gettext("user_expired")}, 401)
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return ({"access_token": access_token, "refresh_token": refresh_token, "user_id": user.id}, 200)
        return ({'message': gettext("user_not_found")}, 404)
