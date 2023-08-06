class Quadrado:
    pass


class Branco(Quadrado):
    def __str__(self):
        return ' '


class Preto(Quadrado):
    def __init__(self, utf8: bool = True):
        self.utf8 = utf8

    def __str__(self):
        return '·' if self.utf8 else '*'
