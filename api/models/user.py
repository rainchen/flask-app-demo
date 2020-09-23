from api.datab import db
from api.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = db.Column(db.String(80), primary_key=True, default="234")
    first_name = db.Column(db.String(length=50), nullable=False)
    last_name = db.Column(db.String(length=50), nullable=False)
    username = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)
