class Peca:

    def __init__(self, pos: tuple):
        self.pos = pos
        self.__dama = False

    def movimentar(self, new_pos: tuple):
        self.pos = new_pos

    def virar_dama(self):
        self.__dama = True

    def is_dama(self):
        return self.__dama


class Branca(Peca):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def __str__(self):
        return 'B' if self.is_dama() else 'b'


class Preta(Peca):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def __str__(self):
        return 'P' if self.is_dama() else 'p'
