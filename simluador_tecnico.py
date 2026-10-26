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

    PONTOS_SET = 25
    PONTOS_TIE_BREAK = 15
    SETS_PARA_VENCER = 3

    def __init__(self, times: list[Time]):
        self.times = times
        self.pontos = {times[0]: 0, times[1]: 0}
        self.sets = {times[0]: 0, times[1]: 0}

    def aumentar_pontos(self, time: Time):
        self.pontos[time] += 1

    def aumentar_sets(self, time: Time):
        self.sets[time] += 1

    def zerar_pontos(self):
        for time in self.pontos:
            self.pontos[time] = 0

    def set_em_andamento(self):
        """Retorna True se o set não acabou"""
        pontos = list(self.pontos.values())

        if sum(self.sets.values()) < 2 * (self.SETS_PARA_VENCER - 1):
            max_pontos = self.PONTOS_SET
        else:
            max_pontos = self.PONTOS_TIE_BREAK

        return max(pontos) < max_pontos or max(pontos) - min(pontos) < 2

    def partida_em_andamento(self):
        """Retorna True se a partida não acabou"""
        return max(self.sets.values()) < self.SETS_PARA_VENCER


class Partida:
    """Classe que comandará a partida"""
    def __init__(self, placar: Placar):
        self.placar = placar
        self.times = self.placar.times

    def jogar_moeda(self):
        return random.randint(0, 1)

    def disputar_partida(self):
        indice = self.jogar_moeda()
        time_sacador = self.times[indice]
        time_receptor = self.times[1 - indice]

        while self.placar.partida_em_andamento():
            sacador = time_sacador.escolher_sacador()
            qualidade_saque = sacador.sacar()
            receptor = time_receptor.escolher_receptor()
            qualidade_passe = receptor.receber(qualidade_saque)

            while self.placar.set_em_andamento():
                levantador = time_receptor.escolher_levantador()
                qualidade_levantamento = levantador.levantar(qualidade_passe)
                atacante = time_receptor.escolher_atacante()
                qualidade_ataque = atacante.atacar(qualidade_levantamento)
                bloqueador = time_sacador.escolher_bloqueador()
                qualidade_bloqueio = bloqueador.bloquear(qualidade_ataque)
                defensor = time_sacador.escolher_defensor()
                qualidade_passe = defensor.defender(qualidade_bloqueio)

            self.placar.zerar_pontos()