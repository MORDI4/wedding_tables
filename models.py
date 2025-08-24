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
    
    def get(self, table_num):
        for table in self.tables:
            if table['table_num'] == table_num:
                return table
        return []

    def create(self, data):
        data.pop('csrf_token', None)
        self.tables.append(data)
        self.save_all()

    def save_all(self):
        with open('tables.json', 'w') as f:
            json.dump(self.tables,f)

    def update(self, table_num, data):
        data.pop('csrf_token', None)
        table = self.get(table_num)
        if table:
            index = self.tables.index(table)
            self.tables[index] = data
            self.save_all()
            return True
        return False

    def delete(self, table_num):
        todo = self.get(table_num)
        if todo:
            self.tables.remove(todo)
            self.save_all()
            return True
        return False

tables = Tables()
