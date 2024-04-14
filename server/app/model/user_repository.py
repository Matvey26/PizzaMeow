from argon2 import PasswordHasher
from .repository import Repository
from .models import User, Payment

ph = PasswordHasher()


class UserRepository(Repository):
    def __init__(self):
        Repository.__init__(self, User)

    def create(
            self,
            email: str,
            password: str,
            firstname: str,
            lastname: str,
            phone_number: str,
            address: str
    ):
        return User(
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            phone_number=phone_number,
            address=address
        )
    
    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()
    
    def save(self, user: User):
        user.password = ph.hash(user.password)
        self.session.add(user)
        self.session.commit(user)
    
    def authenticate(self, email: str, password: str) -> bool:
        user = self.get_by_email(email)
        if user and ph.verify(user.password, password):
            return True
        return False
    
    def is_invalid(self, user: User) -> list:
        invalid_fields = []

        if not user.email:
            invalid_fields.append({'email': 'поле email должно содержать значение'})

        if self.get_by_email(user.email):
            invalid_fields.append({'email': 'пользователь с такой почтой уже существует'})

        if not user.password:
            invalid_fields.append({'password': 'поле password должно содержать значение'})
        
        if len(user.password) < 8:
            invalid_fields.append({'password': 'пароль должен быть не короче 8 символов'})

        return invalid_fields