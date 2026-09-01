from bank.repository.account_repository.account_repo import BankAccountRepository
from bank.model.account_model.bank_account_create import BankAccount


class AccountServices:

    @staticmethod
    def create_account(customer, data):

        account_type = data.get('account_type')
        branch_name = data.get('branch_name')

        exist_account = BankAccountRepository.get_account_by_num(
            customer.id, account_type
        )

        if exist_account:
            raise ValueError(
                f"You have already {account_type}"
            )

        bank_account = BankAccount.open_new_account(
            customer = customer,
            account_type = account_type,
            branch_name = branch_name 
        )

        BankAccountRepository.create_account(bank_account)
        return bank_account

    @staticmethod
    def users_accounts():
        return BankAccountRepository.get_all_account()

    @staticmethod
    def user_account(id):
        return BankAccountRepository.get_account(id)

    @staticmethod
    def update_account(account, data):

        account.account_type = data.get("account_type", account.account_type)
        account.branch_name = data.get("branch_name", account.branch_name)

        BankAccountRepository.update_account()
        return account

    @staticmethod
    def remove_account(account):

        BankAccountRepository.delete_account(account)
        return True
        
