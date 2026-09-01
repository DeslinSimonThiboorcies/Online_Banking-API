import secrets

from bank.extensions.db import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError


class AccountType:
    SAVINGS = 'savings'
    CURRENT = 'current'
    FIXED_DEPOSIT = 'fixed_deposit'

    all = [SAVINGS, CURRENT, FIXED_DEPOSIT]


class AccountStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    CLOSED = 'closed'


class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'
    __table_args__ = (
        db.Index('ix_bank_accounts_user_id', 'user_id'),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('customers.id'),
        nullable = False
    )
    account_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True,
    )
    account_type = db.Column(
        db.String(20),
        nullable=False
    )
    balance = db.Column(
        db.Numeric(15, 2),
        default=0.00,
        nullable=False
    )
    branch_name = db.Column(
        db.String(20),
        nullable=False
    )
    status = db.Column(
        db.String(20),
        default=AccountStatus.ACTIVE,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    snapshot_full_name = db.Column(
        db.String(80),
        nullable=False,
    )
    snapshot_username = db.Column(
        db.String(80),
        nullable=False,
    )
    snapshot_phone_number = db.Column(
        db.String(20),
        nullable=True,
    )
    snapshot_email = db.Column(
        db.String(120),
        nullable=False,
    )
    snapshot_address = db.Column(
        db.Text,
        nullable=True,
    )
    snapshot_state = db.Column(
        db.String(80),
        nullable=True,
    )
    snapshot_taken_at = db.Column(
        db.DateTime,
        nullable=True,
        default=datetime.utcnow,
    )

    customer = db.relationship(
        'Customer',
        backref='bank_accounts'
    )

    ACCOUNT_NUMBER_LENGTH = 12
    MAX_GENERATION_ATTEMPTS = 5

    @classmethod
    def _generate_account_number(cls) -> str:
        return ''.join(secrets.choice('0123456789') for _ in range(cls.ACCOUNT_NUMBER_LENGTH))

    @classmethod
    def open_new_account(cls, customer, account_type: str, branch_name: str) -> 'BankAccount':

        if account_type not in AccountType.all:
            raise ValueError(
                f"Invalid account_type '{account_type}'. Must be one of {AccountType.all}."
            )

        if not customer.is_active:
            raise ValueError('Cannot open an account for an inactive customer.')

        last_error = None
        for _ in range(cls.MAX_GENERATION_ATTEMPTS):
            account = cls(
                user_id=customer.id,
                account_number=cls._generate_account_number(),
                account_type=account_type,
                branch_name=branch_name,
                snapshot_full_name=customer.full_name,
                snapshot_username=customer.username,
                snapshot_phone_number=customer.phone_number,
                snapshot_email=customer.email,
                snapshot_address=customer.address,
                snapshot_state=customer.state,
                snapshot_taken_at=datetime.utcnow(),
            )
            db.session.add(account)
            try:
                db.session.flush()  # surfaces the unique-constraint error without committing
                return account
            except IntegrityError as exc:
                db.session.rollback()
                last_error = exc
                continue

        raise RuntimeError(
            f'{cls.MAX_GENERATION_ATTEMPTS} attempts.'
        ) from last_error

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'branch_name': self.branch_name,
            'balance': str(self.balance),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'holder_name': self.snapshot_full_name,
        }

    def __repr__(self):
        return f'<BankAccount {self.account_number} ({self.status})>'