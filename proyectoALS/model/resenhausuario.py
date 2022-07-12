from datetime import datetime

class Resenhausuario:
    def __init__(self, notausr, comentariousr, usuario, fecha):
        self._notausr = notausr
        self._comentariousr = comentariousr
        self._usuario = usuario
        self._fecha = fecha

    @property
    def notausr(self):
        return self._notausr

    @property
    def comentariousr(self):
        return self._comentariousr

    @property
    def usuario(self):
        return self._usuario

    @property
    def fecha(self):
        return self._fecha

    @notausr.setter
    def notausr(self, x):
        self._notausr = x

    @comentariousr.setter
    def comentariousr(self, x):
        self._comentariousr = x

    def __str__(self):
        return "{0}, {1}".format(self.notausr, self.comentariousr)
