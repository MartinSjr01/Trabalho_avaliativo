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
        qualidade = random.uniform(1, 100)
        return qualidade

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
        
        possiveis_levantadores = self.rotacao.remove(passador) #ele escolhe quem vai levantar excluindo quem passou
        
        return random.choices(
            possiveis_levantadores,
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

        possiveis_atacantes = self.rotacao.remove(levantador) #ele escolhe quem vai atacar excluindo quem levantou
        
        return random.choices(
        possiveis_atacantes,
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

        possiveis_bloqueadores = self.rotacao.remove(0,4,5) #ele nao deixa quem esta na parte de fundo de quadra bloquear

        return random.choices(
                possiveis_bloqueadores,
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

        possiveis_defensores = self.rotacao.remove(bloqueadores) #ele nao deixa o bloqueador defender, e deixa quem nao foi bloquear defender
        
        return random.choices(
            possiveis_defensores,
            weights=[pesos[j.posicao] for j in self.rotacao],
               )[0]

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