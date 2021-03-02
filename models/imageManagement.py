from db import db


class ImageModel(db.Model):
    __tablename__ = "images"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(70), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")




    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
