import traceback
from flask_restful import Resource, reqparse
from flask import request
from werkzeug.security import safe_str_cmp
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import (
    jwt_required,
    create_refresh_token,
    create_access_token,
    jwt_refresh_token_required,
    get_jwt_identity, )

from schemas.imageManagement import ImageSchema
from models.imageManagement import ImageModel
from models.user import UserModel
from libs.strings import gettext
from imageFileManager.petImages import storage_folder, pet_image_saving_directory
from werkzeug.utils import secure_filename

pet_image_schema = ImageSchema()


class ImageUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "file", type=FileStorage, location='files', required=True, help="this field can not be left blank"
    )
    parser.add_argument(
        "pet_type", type=str, required=True, help="this field can not be left blank"
    )

    @classmethod
    @jwt_required
    def post(cls):
        data = cls.parser.parse_args()
        filename = secure_filename(data["file"].filename)
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        image = pet_image_saving_directory(data["pet_type"], data['file'], user_id)
        print(image)
        pet_image = pet_image_schema.load({'image_path': image['image_path'], 'user_id':user_id})

        pet_image.save_to_db()

        return {"message": "file saved"}, 200
