from model.userdto import UserDto

"""Usuarios críticos"""
def usuarioscriticos():
    users = []
    users.append(UserDto("sony", "1234", "admin"))
    users.append(UserDto("xbox", "1234", "admin"))
    users.append(UserDto("admin", "1234", "admin"))
    users.append(UserDto("critic", "1234", "admin"))
    users.append(UserDto("god", "1234", "admin"))
    users.append(UserDto("sega", "1234", "admin"))
    return users
