from datetime import datetime

class Resenhacritica:
    def __init__(self, notacrit, comentariocrit, usuario, fecha):
        self._notacrit = notacrit
        self._comentariocrit = comentariocrit
        self._usuario = usuario
        self._fecha = fecha

    @property
    def notacrit(self):
        return self._notacrit

    @property
    def comentariocrit(self):
        return self._comentariocrit

    @property
    def usuario(self):
        return self._usuario

    @property
    def fecha(self):
        return self._fecha

    @notacrit.setter
    def notacrit(self, x):
        self._notacrit = x

    @comentariocrit.setter
    def comentariocrit(self, x):
        self._comentariocrit = x

    def __str__(self):
        return "{0}, {1}".format(self.notacrit, self.comentariocrit)
