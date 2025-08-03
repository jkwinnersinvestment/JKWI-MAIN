class Division:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def update_description(self, new_description):
        self.description = new_description

    def __str__(self):
        return f"Division {self.name} (ID: {self.id}): {self.description}"