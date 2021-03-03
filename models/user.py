from db import db
from models.confirmation import ConfirmationModel
from models.petImage import PetImageModel


class UserModel(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic",
        cascade="all, delete-orphan")

    images = db.relationship("PetImageModel", lazy="dynamic", cascade="all, delete-orphan")

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(
            username=username
        ).first()  # SELECT * FROM ITEMS WHERE name = name ile aynı işi yapıyor , id 1 yaprak ilk sonucu al dediks

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(
            id=_id
        ).first()  # SELECT * FROM ITEMS WHERE name = name ile aynı işi yapıyor , id 1 yaprak ilk sonucu al dediks

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email
                                   ).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
