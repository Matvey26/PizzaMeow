from argon2 import PasswordHasher, exceptions
from .repository import Repository
from .models import User, UserConfirmEnum

ph = PasswordHasher()


class UserRepository(Repository):
    def __init__(self):
        Repository.__init__(self, User)

    def create(
            self,
            email: str,
            password: str,
            firstname: str = None,
            lastname: str = None,
            phone_number: str = None,
            address: str = None,
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
        self.session.commit()

    def change_password(self, user: User, new_password: str):
        user.password = ph.hash(new_password)

    def change_email(self, user: User, new_email: str):
        user.email = new_email
    
    def authenticate(self, email: str, password: str) -> bool:
        user = self.get_by_email(email)
        if user is None:
            return False
        try:
            ph.verify(user.password, password)
            return True
        except exceptions.VerifyMismatchError:
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

    def is_confirmed(self, user: User):
        return user._confirmed == UserConfirmEnum.CONFIRMED
    
    def mark_as_confirmed(self, user: User):
        user._confirmed = UserConfirmEnum.CONFIRMED