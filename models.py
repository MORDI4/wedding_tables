import json

class Tables:
    def __init__(self):
        try:
            with open('tables.json', 'r') as f:
                self.tables = json.load(f)
        except FileNotFoundError:
            self.tables = []
    
    def all(self):
        return self.tables
    
    def get(self, num):
        return self.tables[num]

    def create(self, data):
        data.pop('csrf_token')
        self.tables.append(data)

    def save_all(self):
        with open('tables.json', 'w') as f:
            json.dump(self.tables,f)

    def update(self, num, data):
        data.pop('csrf_token')
        self.tables[num] = data
        self.save_all()

tables = Tables()
