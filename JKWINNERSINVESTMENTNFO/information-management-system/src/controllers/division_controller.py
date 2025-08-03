class DivisionController:
    def __init__(self, division_service):
        self.division_service = division_service

    def create_division(self, name, description):
        return self.division_service.create_division(name, description)

    def get_division(self, division_id):
        return self.division_service.get_division(division_id)

    def list_divisions(self):
        return self.division_service.list_divisions()