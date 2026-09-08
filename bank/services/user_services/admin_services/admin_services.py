from bank.repository.user_repository.admin_repo import AdminRepository

class AdminServices:

    @staticmethod
    def view_admin(admin_id):

        return AdminRepository.get_admin_by_id(admin_id)

    @staticmethod
    def update(admin, data):

        admin.full_name = data.get("full_name", admin.full_name)
        admin.phone_number = data.get("phone_number", admin.phone_number)
        admin.email = data.get("email",admin.email)
        admin.date_of_birth = data.get("date_of_birth", admin.date_of_birth)
        admin.username = data.get("username", admin.username)
        admin.address = data.get("address", admin.address)
        admin.state = data.get("state", admin.state)
        admin.country = data.get("country", admin.country)
        admin.zip_code = data.get("zip_code", admin.zip_code)


        AdminRepository.update_admin()
        return admin

    @staticmethod
    def delete(admin):

        AdminRepository.delete_admin(admin)
        return True
    