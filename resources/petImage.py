import time
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import (
    jwt_required,
    create_refresh_token,
    create_access_token,
    jwt_refresh_token_required,
    get_jwt_identity, )
from schemas.petImage import PetImageSchema
from libs.strings import gettext
from imageFileManager.petImagesManager import pet_image_saving_directory

pet_image_schema = PetImageSchema()

'''pet image upload sınıfı / görüntüyü file systeme ve databaseye kaydeder'''

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PetImageUpload(Resource):
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
        if data and allowed_file(data["file"].filename):
            user_id = get_jwt_identity()
            ms_time = time.time() * 1000
            image = pet_image_saving_directory(data["pet_type"], data['file'], user_id, ms_time)
            pet_image = pet_image_schema.load({'image_path': image['image_path'], 'user_id': user_id})
            pet_image.save_to_db()
            return {"message": gettext("image_upload_successfully")}, 200
        return {"message": gettext("not_allowed_image_extension")}, 400
