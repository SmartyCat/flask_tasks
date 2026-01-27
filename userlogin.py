from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = (
            db.cursor()
            .execute("SELECT * FROM users WHERE id = ?", (user_id,))
            .fetchone()
        )
        return self

    @property
    def username(self) -> str:
        return self.__user[1]

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user[0])
