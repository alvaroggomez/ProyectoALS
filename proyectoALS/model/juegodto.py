

class JuegoDto:
    def __init__(self, titulo, resumen, autor, imagen, nota):
        self._titulo = titulo
        self._resumen = resumen
        self._autor = autor
        self._imagen = imagen
        self._nota = nota
        self._resenhacriticas = []
        self._resenhausuarios = []
        self._notascrit = []
        self._notasusr = []
        self._medianotacrit = 0
        self._medianotausr = 0

    @property
    def titulo(self):
        return self._titulo

    @property
    def resumen(self):
        return self._resumen

    @property
    def autor(self):
        return self._autor

    @property
    def imagen(self):
        return self._imagen

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, n):
        self._nota = n

    @property
    def resenhacriticas(self):
        if not self.__dict__.get("_resenhacriticas"):
            self._resenhacriticas = []
        return self._resenhacriticas

    @property
    def resenhausuarios(self):
        if not self.__dict__.get("_resenhausuarios"):
            self._resenhausuarios = []
        return self._resenhausuarios

    @property
    def medianotacrit(self):
        return self._medianotacrit

    @medianotacrit.setter
    def medianotacrit(self, n: int):
        self._medianotacrit = n

    @property
    def medianotausr(self):
        return self._medianotausr

    @medianotausr.setter
    def medianotausr(self, n: int):
        self._medianotausr = n

    def add_resenhacriticas(self, comentario):
        self.resenhacriticas.append(comentario)

    def add_resenhausuarios(self, comentario):
        self.resenhausuarios.append(comentario)

    def del_resenhacriticas(self, comentario_indice):
        self.resenhacriticas.remove(comentario_indice)

    def del_resenhausuarios(self, comentario_indice):
        self.resenhausuarios.remove(comentario_indice)

    def agregaycalculanotacrit(self, n) -> int:
        self._notascrit.append(n)
        num_notascrit = len(self._notascrit)
        media = sum(self._notascrit) / num_notascrit if num_notascrit > 0 else 0
        return int(media)

    def eliminaycalculanotacrit(self, n) -> int:
        self._notascrit.remove(n)
        num_notascrit = len(self._notascrit)
        media = sum(self._notascrit) / num_notascrit if num_notascrit > 0 else 0
        return int(media)

    def agregaycalculanotausr(self, n) -> int:
        self._notasusr.append(n)
        num_notasusr = len(self._notasusr)
        media = sum(self._notasusr) / num_notasusr if num_notasusr > 0 else 0
        return int(media)

    def eliminaycalculanotausr(self, n) -> int:
        self._notasusr.remove(n)
        num_notasusr = len(self._notasusr)
        media = sum(self._notasusr) / num_notasusr if num_notasusr > 0 else 0
        return int(media)


    def __str__(self):
        return f"{self.titulo}\n{self.resumen}"

