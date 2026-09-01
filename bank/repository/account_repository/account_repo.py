from bank.model.account_model.bank_account_create import BankAccount
from bank.extensions.db import db


class BankAccountRepository:


    @staticmethod
    def create_account(account):
        db.session.add(account)
        db.session.commit()

    @staticmethod
    def get_all_account():
        return BankAccount.query.all()

    @staticmethod
    def get_account_by_id(user_id, account_type):
        BankAccount.query.filter_by(
            user_id = user_id,
            account_type = account_type
        ).first()

    @staticmethod
    def get_account(account_id):
        db.session.get(
            BankAccount,
            account_id
        )

    @staticmethod
    def update_account():
        db.session.commit()

    @staticmethod
    def delete_account(account):
        db.session.delete(account)
        db.session.commit()