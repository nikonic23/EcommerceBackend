import bcrypt
from flask_jwt_extended import create_access_token
from utils.helpers import get_cursor
from extensions import mysql
from repositories.user_repository import UserRepository


def register_user(name, email, password):
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    UserRepository.create(name, email, hashed_password)


def authenticate_user(email,password):
    user = UserRepository.get_by_email(email)

    if not user:
        return None
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    ):
        return None
    return user


def generate_access_token(user):
    return create_access_token(
        identity=str(user['id']),
        additional_claims={"role": user["role"]}
    )