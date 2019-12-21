from database.user_db import UserModel


def authenticate(username, password):
    try:
        user = UserModel.find_by_username(username)
        if user and user.password == password:
            return user
        return None
    except Exception as e:
        raise Exception(e)

