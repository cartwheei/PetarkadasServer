from ma import ma
from models.imageManagement import ImageModel


class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ImageModel
        load_instance = True
        include_fk = True