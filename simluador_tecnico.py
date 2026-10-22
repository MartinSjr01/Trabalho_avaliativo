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
    """Classe que decide o jogador que executa ações"""
    def __init__(self, jogadores: list[Jogador], tecnicos: list[Tecnico]):
        self.jogadores = jogadores
        self.rotacao = jogadores[:6]
        self.tecnicos = tecnicos

    def rodar(self):
        """Sentido horário: o jogador da posição 2 vai para o saque"""
        self.rotacao = self.rotacao[1:] + self.rotacao[:1]

    def escolher_sacador(self) -> Jogador:
        return self.rotacao[0]

    def escolher_receptor(self) -> Jogador:
        pesos = {
            Posicao.PONTEIRO: 45,
            Posicao.LIBERO: 50,
            Posicao.OPOSTO: 1.5,
            Posicao.CENTRAL: 3,
            Posicao.LEVANTADOR: 0.5,
        }
        return random.choices(
            self.rotacao,
            weights=[pesos[j.posicao] for j in self.rotacao],
        )[0]

    def escolher_levantador(self, passador: Jogador) -> Jogador:
        pesos = {
            Posicao.PONTEIRO: 6,
            Posicao.LIBERO: 15,
            Posicao.OPOSTO: 1,
            Posicao.CENTRAL: 8,
            Posicao.LEVANTADOR: 70,
            }
        return random.choices(
            self.rotacao,
            weights=[pesos[j.posicao] for j in self.rotacao],
        )[0]

    def escolher_atacante(self, levantador: Jogador) -> Jogador:
        pesos = {
            Posicao.PONTEIRO: 35,
            Posicao.LIBERO: 0,
            Posicao.OPOSTO: 40,
            Posicao.CENTRAL: 20,
            Posicao.LEVANTADOR: 5,
            }
        return random.choices(
        self.rotacao,
        weights=[pesos[j.posicao] for j in self.rotacao],
         )[0]

    def escolher_bloqueadores(self) -> list[Jogador]:
        pesos = {
            Posicao.PONTEIRO: 15,
            Posicao.LIBERO: 0,
            Posicao.OPOSTO: 15,
            Posicao.CENTRAL: 60,
            Posicao.LEVANTADOR: 10,
            }
        return random.choices(
                self.rotacao,
                weights=[pesos[j.posicao] for j in self.rotacao],
                )[0]

    def escolher_defensor(self, bloqueadores: list[Jogador]) -> Jogador:
        pesos = {
            Posicao.PONTEIRO: 25,
            Posicao.LIBERO: 40,
            Posicao.OPOSTO: 14,
            Posicao.CENTRAL: 5,
            Posicao.LEVANTADOR: 16,
            }
        return random.choices(
            self.rotacao,
            weights=[pesos[j.posicao] for j in self.rotacao],
               )[0]

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
