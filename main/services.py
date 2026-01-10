from utils.helpers import get_cursor
from flask_jwt_extended import get_jwt, get_jwt_identity
from repositories.user_repository import UserRepository


def get_identity():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims["role"]

    user = UserRepository.get_by_email(user_id)

    return user, role
