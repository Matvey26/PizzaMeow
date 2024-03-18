
class Model:

    def serialize(self)->dict:
        return {}


class Card(Model):
    def __init__(self, numbercard=None, name=None, surname=None, code=None, data=None):
        if numbercard == None or name == None or surname == None or code == None or data == None:
            self.initialized = False
        else:
            self.initialized = True
        self.numbercard = numbercard
        self.name = name
        self.surname = surname
        self.code = code
        self.data = data
    def __repr__(self):
        return f"{self.numbercard}\n {self.name} {self.surname}   {self.code}\n {self.data}"

class Order(Model):
    def __init__(self, id, ingridients, result_price=0):
        self.id = id
        self.ingridients = ingridients
        for key in ingrients:
            self.result_price += ingridients[key]
        
    
class User(Model):
    id = 0
    def __init__(self, login=None, email=None, password=None):
        self.id = id
        id += 1
        self.email = email
        self.login = login
        self.password = password
        self.name = None
        self.surname = None
        self.adress = None
        self.card = Card()
        self.user_history = list()
