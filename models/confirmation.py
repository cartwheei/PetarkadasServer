from time import time
from uuid import uuid4

from db import db

CONFIRMATION_EXPIRATION_DELTA = 1800  # 30 minutes


class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = True

    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, user_id: int) -> "ConfirmationModel":
        return cls.query.filter_by(user_id=user_id).first()



    @property  # buraya property yazarak bu fonksiyonu bir öznitelik olarak cagırabiliyoruz
    def expired(self) -> bool:
        return time() > self.expire_at

    def force_to_expire(self) -> None:  # forcing current confirmation to expire
        print(self.expired)
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()

    def change_expire_date(self) -> None:
        self.expire_at = int(time())+CONFIRMATION_EXPIRATION_DELTA
        self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
