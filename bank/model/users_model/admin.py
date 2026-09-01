from bank.extensions.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Admin(db.Model):

    __tablename__ = 'admin'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    full_name = db.Column(
        db.String(80),
        nullable=False,
    )
    phone_number = db.Column(
        db.String(20),
        unique=True,
        nullable=True,
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
    )
    date_of_birth = db.Column(
        db.Date,
        nullable = False
    )
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )
    role = db.Column(
        db.String,
        default='admin',
        nullable=False,
    )
    address = db.Column(
        db.Text,
        nullable=True,
    )
    state = db.Column(
        db.String(80),
        nullable = False
    )
    country = db.Column(
        db.String(80),
        nullable = False,
    )
    zip_code = db.Column(
        db.Integer,
        nullable = False
    )
    password = db.Column(
            db.String(225),
            nullable=False,
        )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )
    login_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    

    def admin_password(self, password):
        self.password = generate_password_hash(password)

    def check_admin_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Admin {self.full_name}>'