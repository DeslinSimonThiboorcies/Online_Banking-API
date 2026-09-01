from bank.extensions.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    full_name = db.Column(
        db.String(80),
        nullable=False,
    )
    phone_number = db.Column(
        db.Integer,
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
        nullable=False,
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
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    login_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    def employee_password(self, password):
        self.password = generate_password_hash(password)

    def check_employee_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Employee {self.full_name}>'