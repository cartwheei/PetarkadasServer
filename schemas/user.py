from marshmallow import pre_dump, post_dump, pre_load
from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")
        load_instance = True
        include_fk = True


    # @pre_dump
    # def _pre_dump(self, user: UserModel, **kwargs):
    #     user.confirmation = [user.most_recent_confirmation]
    #     return user
