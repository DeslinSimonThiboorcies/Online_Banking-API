from bank.extensions.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class CustomerSupport(db.Model):
    __tablename__ = 'customer_support'

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
        nullable=True,
    )
    address = db.Column(
        db.Text,
        nullable=True,
    )
    state = db.Column(
        db.String(80),
        nullable=True,
    )
    country = db.Column(
        db.String(80),
        nullable=True,
    )
    zip_code = db.Column(
        db.String(20),
        nullable=True,
    )
    role = db.Column(
        db.String,
        default='customer_support',
        nullable=False,
    )
    language = db.Column(
        db.String(80),
        nullable=True,
    )
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
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

    def customer_support_password(self, password):
        self.password = generate_password_hash(password)

    def check_customer_support_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<CustomerSupport {self.full_name}>'