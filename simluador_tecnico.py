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
        ...

    def pedir_tempo(self):
        ...


class Jogador:
    """Definição da classe Jogador"""
    def __init__(self, nome: str, camisa: int, posicao: Posicao):
        self.nome = nome
        self.camisa = camisa
        self.posicao = posicao

    def sacar(self):
        ...

    def receber(self):
        ...

    def levantar(self):
        ...

    def atacar(self):
        ...

    def bloquear(self):
        ...

    def defender(self):
        ...

    
class Time:
    """Definição da classe Time"""
    def __init__(self, jogadores: list[Jogador]):
        self.jogadores = jogadores
        self.rotacao = jogadores[:6]


class Partida:
    """Definição da classe Partida"""
    def __init__(self, tecnicos: Tecnico, times: list[Time]):
        self.tecnicos = tecnicos
        self.times = times

    def iniciar_partida(self):
        self.times[random.randint(0, 1)].jogadores.sacar()