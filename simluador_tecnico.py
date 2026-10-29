import random
from enum import Enum


class Posicao (Enum):
    LEVANTADOR = 1
    OPOSTO = 2
    PONTEIRO = 3
    CENTRAL = 4
    LIBERO = 5


class Tecnico:
    """Definição da classe Tecnico"""
    def __init__(self, nome: str):
        self.nome = nome

    def substituir(self):



class Jogador:
    """Classe que executa ações"""
    def __init__(self, nome: str, camisa: int, posicao: Posicao):
        self.nome = nome
        self.camisa = camisa
        self.posicao = posicao

    def sacar(self):
        ...

    def receber(self, qualidade: float):
        return random.triangular(1, 100, mode = 100 - qualidade)

    def levantar(self, qualidade: float):
        return random.triangular(1, 100, mode = qualidade)

    def atacar(self, qualidade: float):
        return random.triangular(1, 100, mode = qualidade)

    def bloquear(self, qualidade: float):
        return random.triangular(1, 100, mode = 100 - qualidade)

    def defender(self, qualidade: float):
        return random.triangular(1, 100, mode = qualidade)

    
class Time:
    """Classe que decide o jogador que executa ações"""
    class Time:
    def __init__(self, jogadores: list[Jogador], tecnicos: list[Tecnico]):
        self.jogadores = jogadores
        self.rotacao = jogadores[:6]
        self.tecnicos = tecnicos
        self.tempos_restantes = 2
        self.substituicoes_restantes = 6

    def escolher_sacador(self):
        self.rotacao[0].sacar()

    def escolher_receptor(self):
        self.rotacao[random.randint(0, 5)].receber() # por enquanto um jogador aleatório, depois, adionar mais probablidade dos ponteiros e do líbero receberem

    def esolher_levantador(self):
        ...

    def escolher_atacante(self):
        ...

    def escolher_bloqueador(self):
        ...

    def escolher_defensor(self):
        ...


class Partida:
    """Classe que comandará a partida"""
    def __init__(self, times: list[Time]):
        self.times = times

    def jogar_moeda(self):
        self.iniciar_set(self, random.randint(0, 1))

    def iniciar_set(self, indice):
        time_sacador = self.times[indice]
        time_receptor = self.times[1 - indice]

        time_sacador.escolher_sacador()
        time_receptor.escolher_receptor()
