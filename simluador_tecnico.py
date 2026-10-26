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
    """Classe que executa ações"""
    def __init__(self, nome: str, camisa: int, posicao: Posicao):
        self.nome = nome
        self.camisa = camisa
        self.posicao = posicao

    def sacar(self):
        qualidade = random.uniform(1, 100)
        return qualidade

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
    """Classe que decide o jogador que executa ações"""
    def __init__(self, jogadores: list[Jogador], tecnicos: list[Tecnico]):
        self.jogadores = jogadores
        self.rotacao = jogadores[:6]
        self.tecnicos = tecnicos

    def escolher_sacador(self):
        return self.rotacao[0]

    def escolher_receptor(self):
        self.rotacao[random.randint(0, 5)].receber() # por enquanto um jogador aleatório, depois, adionar mais probablidade dos ponteiros e do líbero receberem

    def escolher_levantador(self):
        ...

    def escolher_atacante(self):
        ...

    def escolher_bloqueador(self):
        ...

    def escolher_defensor(self):
        ...

class Placar:
    """Classe que contabilizará os pontos e sets"""
    def __init__(self):
        self.pontos = [0, 0]
        self.sets = [0, 0]

    def aumentar_pontos(self, indice_time: int):
        self.pontos[indice_time] += 1

    def aumentar_sets(self, indice_time: int):
        self.sets[indice_time] += 1

    def set_em_andamento(self):
        """Retorna True se o set não acabou"""
        return (self.pontos[0] < 25 or self.pontos[1] < 25) or abs(self.pontos[0] - self.pontos[1]) < 2

    def partida_em_andamento(self):
        """Retorna True se a partida não acabou"""
        return self.sets[0] < 3 and self.sets[1] < 3


class Partida:
    """Classe que comandará a partida"""
    def __init__(self, times: list[Time], placar: Placar):
        self.times = times
        self.placar = placar

    def jogar_moeda(self):
        return random.randint(0, 1)

    def disputar_partida(self):
        indice_sacador = self.jogar_moeda()
        indice_receptor = 1 - indice_sacador

        while self.placar.partida_em_andamento():
            sacador = self.times[indice_sacador].escolher_sacador()
            qualidade_saque = sacador.sacar()
            receptor = self.times[indice_receptor].escolher_receptor()
            qualidade_passe = receptor.receber(qualidade_saque)

            while self.placar.set_em_andamento():
                levantador = self.times[indice_receptor].escolher_levantador()
                qualidade_levantamento = levantador.levantar(qualidade_passe)
                atacante = self.times[indice_receptor].escolher_atacante()
                qualidade_ataque = atacante.atacar(qualidade_levantamento)
                bloqueador = self.times[indice_sacador].escolher_bloqueador()
                qualidade_bloqueio = bloqueador.bloquear(qualidade_ataque)
                defensor = self.times[indice_sacador].escolher_defensor()
                qualidade_passe = defensor.defender(qualidade_bloqueio)