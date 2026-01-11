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

    
    @staticmethod
    def get_by_id(user_id):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
