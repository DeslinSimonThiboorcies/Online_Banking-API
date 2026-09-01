from bank.repository.user_repository.manager_repo import ManagerRepository

class MangerService:

    @staticmethod
    def view_managers():
        return ManagerRepository.get_manager()

    @staticmethod
    def view_manager(manager_id):
        return ManagerRepository.get_manager_by_id(manager_id)

    @staticmethod
    def update(manager, data):

        manager.full_name = data.get("full_name", manager.full_name)
        manager.phone_number = data.get("phone_number", manager.phone_number)
        manager.email = data.get("email",manager.email)
        manager.address = data.get("address", manager.address)
        manager.date_of_birth = data.get("date_of_birth", manager.date_of_birth)
        manager.state = data.get("state", manager.state)
        manager.country = data.get("country", manager.country)
        manager.zip_code = data.get("zip_code", manager.zip_code)
        manager.username = data.get("username", manager.username)

        ManagerRepository.update_manager()
        return manager

    @staticmethod
    def delete(manager):

        ManagerRepository.delete_manager(manager)
        return True
    