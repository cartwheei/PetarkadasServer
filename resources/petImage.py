import datetime
from flask_restful import Resource, reqparse
from flask import request
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


def allowed_file2(filename):
    return str(filename).rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PetImageUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "pet_type", type=str, required=True, help="this field can not be left blank")

    @classmethod
    @jwt_required
    def post(cls):
        data = cls.parser.parse_args()
        img = request.files

        if data and allowed_file(img['file'].filename):
            user_id = get_jwt_identity()
            # burayı daha sonra gözden geçir
            (dt, micro), utctime = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split(
                '.'), datetime.datetime.utcnow
            micro_time = "%s.%03d" % (dt, int(micro))

            image = pet_image_saving_directory(data["pet_type"], img['file'], user_id, micro_time)
            pet_image = pet_image_schema.load({'image_path': image['image_path'], 'user_id': user_id,
                                               })
            pet_image.save_to_db()
            return {"message": gettext("image_upload_successfully")}, 200
        return {"message": gettext("not_allowed_image_extension")}, 400
