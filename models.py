from flask_login import UserMixin
from app import db


class UserDB(UserMixin, db.Model):
    __tablename__ = "UserDB"
    user_id = db.Column(db.Float, unique=True, primary_key=True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    pic = db.Column(db.String(120))

    def __repr__(self):
        return "<User_id = %s, Email = %s, Name = %s, Pic = %s>" % (
            self.user_id,
            self.email,
            self.name,
            self.pic,
        )

    def get_id(self):
        """Return the id from the username."""
        return self.user_id

    def is_active(self):
        """True, as all users are active."""
        return True
