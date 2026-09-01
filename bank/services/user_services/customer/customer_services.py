from bank.repository.user_repository.customer_repo import CustomerRepository

class CustomerServices:

    @staticmethod
    def view_all_user():

        return CustomerRepository.get_customers()

    @staticmethod
    def view_user(customer_id):
        return CustomerRepository.get_customer_by_id(customer_id)

    @staticmethod
    def update(customer, data):

       customer.full_name = data.get("full_name", customer.full_name)
       customer.phone_number = data.get("phone_number", customer.phone_number)
       customer.email = data.get("email", customer.email)
       customer.address = data.get("address", customer.address)
       customer.date_of_birth = data.get("date_of_birth", customer.date_of_birth)
       customer.state = data.get("state", customer.state)
       customer.country = data.get("country", customer.country)
       customer.zip_code = data.get("zip_code", customer.zip_code)
       customer.username = data.get("username", customer.username)

       CustomerRepository.update_customer()
       return customer

    @staticmethod
    def delete(customer):

        CustomerRepository.delete_customer(customer)
        return True