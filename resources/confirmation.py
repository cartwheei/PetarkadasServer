from time import time

from flask_restful import Resource
from flask import make_response, render_template
import traceback

from models.user import UserModel
from models.confirmation import ConfirmationModel
from schemas.confirmation import ConfirmationSchema
from libs.strings import gettext

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        """return confirmation html page"""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)

        if not confirmation:
            return {"message": gettext("confirmation_not_found")}, 404

        if confirmation.expired:
            return {"message": gettext("confirmation_link_expired")}, 400

        # if confirmation:
        #     confirmation.confirmed = True
        #     confirmation.save_to_db()
        #     return {"message": ALREADY_CONFIRMED}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()
        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers, )


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """returns confirmation for given a user. Use for testing"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        return (
            {"current_time": int(time()),
             "confirmation": [
                 confirmation_schema.dump(each)
                 for each in user.confirmation.order_by(ConfirmationModel.expire_at)], }, 200)

    @classmethod
    def post(cls, user_id):
        """resend confirmation email"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        try:
            cofirmation = user.most_recent_confirmation
            if cofirmation:
                if cofirmation.confirmed:
                    return {"message": gettext("confirmation_already_confirmed")}, 400
                cofirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)  # create a new confirmation
            new_confirmation.save_to_db()
            # Does `user` object know the new confirmation by now? Yes.
            # An excellent example where lazy='dynamic' comes into use.
            user.send_confirmation_email()  # re-send the confirmation email
            return {"message": gettext("confirmation_resend_successful")}, 201


        except:
            traceback.print_exc()
            return {"message": gettext("confirmation_resend_fail")}, 500
