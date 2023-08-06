import damas.peca as peca
import damas.quadrado as quadrado


class Tabuleiro:

    def __init__(self, utf8: bool = True):
        if not isinstance(utf8, bool):
            raise TypeError('O parâmetro "utf8" precisa ser do tipo "bool"')

        self.__is_utf8 = utf8
        self.__tabuleiro = self.__criar_tabuleiro()

        self.__hor = '─' if self.__is_utf8 else '-'
        self.__ver = '│' if self.__is_utf8 else '|'
        self.__qes = '┌' if self.__is_utf8 else '+'  # Quina Esquerda Superior
        self.__qds = '┐' if self.__is_utf8 else '+'  # Quina Direita Superior
        self.__qei = '└' if self.__is_utf8 else '+'  # Quina Esquerda Inferior
        self.__qdi = '┘' if self.__is_utf8 else '+'  # Quina Direita Inferior

    def __str__(self):
        s = self.__qes.rjust(4) + self.__hor*24 + self.__qds + '\n'

        for i in range(8):
            linha = f' {8 - i} {self.__ver}'
            for j in range(8):
                linha += f' {str(self.__tabuleiro[i][j])} ' if j != 7 else f' {str(self.__tabuleiro[i][j])} {self.__ver}'

            s += linha + '\n'

        s += self.__qei.rjust(4) + self.__hor*24 + self.__qdi + '\n'
        s += '     A  B  C  D  E  F  G  H'

        return s

    def __getitem__(self, coord: str):
        if self.__is_valid_coord(coord):
            i, j = self.__coord_to_index(coord)
            return self.__tabuleiro[i][j]

        return False

    def __setitem__(self, coord_init: str, coord_fim: str):
        return self.mover_peca(coord_init.upper(), coord_fim.upper())

    def is_quad_preto(self, coord: str):
        return isinstance(self[coord], quadrado.Preto)

    def is_peca(self, coord: str):
        return isinstance(self[coord], (peca.Branca, peca.Preta))

    def mov_possiveis_peca(self, coord: str):
        if self.is_peca(coord):
            moves = []

            if not self[coord].is_dama():
                sign = self.__sign(coord)
                i, j = self.__coord_to_index(coord)  # Indices da peca escolhida

                moves = self.__da_pra_comer(coord, sign)

                if not moves:
                    for k in [1, -1]:
                        index = (i + 1*sign, j + k)
                        new_coord = self.__index_to_coord(index)

                        if self.__da_pra_andar(new_coord):
                            moves.append(new_coord)

            return sorted(moves)

        return False

    def mov_possiveis_todas(self):
        dict_moves = {}
        flag = True

        for i in range(8):
            for j in range(8):
                coord = self.__index_to_coord((i, j))
                moves = self.mov_possiveis_peca(coord)

                if self.is_peca(coord) and flag and moves:

                    if self.__da_pra_comer(coord, self.__sign(coord)):
                        flag = False
                        dict_moves = {coord: moves}
                    else:
                        dict_moves[coord] = moves

                if not flag:
                    if self.__da_pra_comer(coord, self.__sign(coord)):
                        dict_moves[coord] = moves

        return dict_moves

    def mover_peca(self, coord_init: str, coord_fim: str):
        if self.is_peca(coord_init) and self.is_quad_preto(coord_fim):
            if coord_fim.upper() in self.mov_possiveis_peca(coord_init):
                i, j = self.__coord_to_index(coord_init)
                x, y = self.__coord_to_index(coord_fim)

                self.__tabuleiro[i][j].movimentar((x, y))
                self.__tabuleiro[i][j], self.__tabuleiro[x][y] = self.__tabuleiro[x][y], self.__tabuleiro[i][j]

    def __da_pra_andar(self, coord: str):
        return self.__is_valid_coord(coord) and self.is_quad_preto(coord)

    def __da_pra_comer(self, coord: str, sign):
        moves = []

        i, j = self.__coord_to_index(coord)
        for k in [1, -1]:
            index = (i + 1 * sign, j + k)
            new_cord = self.__index_to_coord(index)

            if self.is_peca(new_cord) and sign != self.__sign(new_cord):
                index = (i + 2*1 * sign, j + 2*k)

                if self.is_quad_preto(self.__index_to_coord(index)):
                    moves.append(self.__index_to_coord(index))

        return moves

    def __sign(self, coord):
        sign = 1

        if isinstance(self[coord], peca.Branca):
            sign = -1

        return sign

    def __criar_tabuleiro(self):

        tabuleiro = []
        for i in range(8):

            linha = []
            for j in range(8):
                if i % 2 == 0 and j % 2 == 1 or i % 2 == 1 and j % 2 == 0:
                    if i in range(3):
                        linha.append(peca.Preta((i, j)))
                    elif i in range(5, 8):
                        linha.append(peca.Branca((i, j)))
                    else:
                        linha.append(quadrado.Preto(self.__is_utf8))
                else:
                    linha.append(quadrado.Branco())

            tabuleiro.append(linha)

        return tabuleiro

    def __coord_to_index(self, coord: str):
        if self.__is_valid_coord(coord):
            i = 8 - int(coord[1])
            j = ord(coord[0].upper()) - 65

            return i, j

    def __index_to_coord(self, index: tuple):
        if self.__is_valid_index(index):
            s = f'{chr(65+index[1])}{8-index[0]}'
            return s

    @staticmethod
    def __is_valid_coord(coord: str):
        if isinstance(coord, str) and len(coord) == 2:
            if coord[1].isnumeric() and coord[0].isalpha():
                if int(coord[1]) in range(1, 9) and coord[0].upper() in 'ABCDEFGH':
                    return True

        return False

    @staticmethod
    def __is_valid_index(index: tuple):
        return len(index) == 2 and index[0] in range(8) and index[1] in range(8)


if __name__ == '__main__':
    # Zona de testes

    tab = Tabuleiro()
    tab['d6'] = 'c5'

    print(tab)
    print(tab.mov_possiveis_todas())

