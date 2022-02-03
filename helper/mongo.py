

class Mongo:
    def __init__(
        self,
        db
    ):
        self.db = db
        self.find_one = db.find_one
        self.find = db.find
        self.insert_one = db.insert_one
        self.update_one = db.update_one
        self.remove = db.delete_one


