from bank.repository.user_repository.customer_sup_reop import CustomerSupportRepository

class CustomerSupportServices:

    @staticmethod
    def view_all_user():

        return CustomerSupportRepository.get_customer_services()

    @staticmethod
    def view_user(id):
        return CustomerSupportRepository.get_customer_support_by_id(id)

    @staticmethod
    def update(customer_support, data):

       customer_support.full_name = data.get("full_name", customer_support.full_name)
       customer_support.phone_number = data.get("phone_number", customer_support.phone_number)
       customer_support.email = data.get("email", customer_support.email)
       customer_support.address = data.get("address", customer_support.address)
       customer_support.date_of_birth = data.get("date_of_birth", customer_support.date_of_birth)
       customer_support.state = data.get("state", customer_support.state)
       customer_support.country = data.get("country", customer_support.country)
       customer_support.zip_code = data.get("zip_code", customer_support.zip_code)
       customer_support.language = data.get("language", customer_support.language)
       customer_support.username = data.get("username", customer_support.username)

       CustomerSupportRepository.update_customer_support()
       return customer_support

    @staticmethod
    def delete(customer_support):

        CustomerSupportRepository.delete_customer_support(customer_support)
        return True