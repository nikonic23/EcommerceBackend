from utils.helpers import get_cursor

class UserRepository:
    @staticmethod
    def get_by_email(email):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def create(name, email, hashed_password):
        cursor = get_cursor()
        cursor.execute(
            "INSERT INTO users(name, email, password) VALUES (%s,%s,%s)",
            (name, email, hashed_password)
        )
        cursor.connection.commit()
        cursor.close()