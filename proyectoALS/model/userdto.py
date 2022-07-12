import sirope
import flask_login
import werkzeug.security as safe


class UserDto(flask_login.UserMixin):
    def __init__(self, usuario, password, access):
        self._usuario = usuario
        self._password = safe.generate_password_hash(password)
        self._access = access

    @property
    def usuario(self):
        return self._usuario

    @property
    def access(self):
        return self._access

    def get_id(self):
        return self._usuario

    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)

    @staticmethod
    def current_user():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        return usr

    @staticmethod
    def find(s: sirope.Sirope, usuario: str) -> "UserDto":
        return s.find_first(UserDto, lambda u: u.usuario == usuario)