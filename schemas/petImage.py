from ma import ma
from models.petImage import PetImageModel

'''pet images şeması'''


class PetImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PetImageModel
        load_instance = True
        include_fk = True
