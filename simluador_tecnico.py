import random
from enum import Enum


class Posicao (Enum):
    """Enumeração das posições"""
    LEVANTADOR = 1
    OPOSTO = 2
    PONTEIRO = 3
    CENTRAL = 4
    LIBERO = 5


class Tecnico:
    """Definição da classe Tecnico"""
    def __init__(self, nome: str, time: Time):
        self.nome = nome
        self.time = time
        self.tempos_restantes = 2
        self.substituicoes_restantes = 6

    def substituir(self, jogador_entrando: Jogador, jogador_saindo: Jogador):
        if self.substituicoes_restates > 0: 
            self.time.rotacao.replace(jogador_saindo, jogador_entrando)
            self.time.reservas.replace(jogador_entrando,jogador_saindo)
            self.substituicoes_restantes -= 1 

    def pedir_tempo(self, ):
        if self.tempos_restantes > 0: 
              ...
              self.tempos_restantes -= 1 


class Jogador:
    """Classe que executa ações"""

    TAMANHO_ATRIBUTOS = 100
    SOMA_ALPHA_BETA = 10
    FATOR_CANSACO = 2 / 3

    def __init__(
            self, nome: str, camisa: int, posicao: Posicao, ataque: float, passe: float,
            levantamento: float, saque: float, bloqueio: float, alcance: float
            ) -> None:
        self.nome = nome
        self.camisa = camisa
        self.posicao = posicao
        self.ataque = ataque
        self.passe = passe
        self.levantamento = levantamento
        self.saque = saque
        self.bloqueio = bloqueio
        self.alcance = alcance
        self.cansaco = 0

    def _medir_qualidade(self, alpha: float) -> float:
        beta = (self.TAMANHO_ATRIBUTOS - alpha) + self.cansaco * self.FATOR_CANSACO
        alpha_n = max(alpha / self.TAMANHO_ATRIBUTOS * self.SOMA_ALPHA_BETA, 1.2)
        beta_n = max(beta / self.TAMANHO_ATRIBUTOS * self.SOMA_ALPHA_BETA, 1.2)
        return random.betavariate(alpha_n, beta_n) * self.TAMANHO_ATRIBUTOS

    def sacar(self) -> float:
        alpha = self.saque
        return self._medir_qualidade(alpha)

    def receber(self, saque_oponente: float) -> float:
        alpha = (3 * self.passe + 2 * (self.TAMANHO_ATRIBUTOS - saque_oponente)) / 5
        return self._medir_qualidade(alpha)

    def levantar(self, passe_aliado: float) -> float:
        alpha = (3 * self.levantamento + 2 * passe_aliado) / 5
        return self._medir_qualidade(alpha)

    def atacar(self, levantamento_aliado: float) -> float:
        alpha = (3 * self.ataque + 2 * levantamento_aliado) / 5
        return self._medir_qualidade(alpha)

    def bloquear(self, ataque_oponente: float) -> float:
        alpha = (2 * self.bloqueio + 5 * (self.TAMANHO_ATRIBUTOS - ataque_oponente)) / 7
        return self._medir_qualidade(alpha)

    def defender(self, ataque_oponente: float, bloqueio_aliado: float) -> float:
        alpha = (3 * self.passe + bloqueio_aliado + 4 * (self.TAMANHO_ATRIBUTOS - ataque_oponente)) / 8
        return self._medir_qualidade(alpha)  

    def cansar(self, valor: int) -> None:
        if self.cansaco + valor <= self.TAMANHO_ATRIBUTOS:
            self.cansaco += valor
        else:
            self.cansaco = self.TAMANHO_ATRIBUTOS

    def descansar(self, valor: int) -> None:
        if self.cansaco - valor >= 0:
            self.cansaco -= valor
        else:
            self.cansaco = 0


class Time:
    """Classe que decide o jogador que executa ações"""
    def __init__(self, jogadores: list[Jogador]) -> None:
        self.jogadores = jogadores
        self.rotacao = jogadores[:6]
        self.reservas = jogadores[6:]

    def rodar(self) -> None:
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


class Placar:
    """Classe que contabilizará os pontos e sets"""

    PONTOS_SET = 25
    PONTOS_TIE_BREAK = 15
    SETS_PARA_VENCER = 3
    VANTAGEM_PARA_VENCER = 2

    def __init__(self, times: list[Time]) -> None:
        self.times = times
        self.pontos = {times[0]: 0, times[1]: 0}
        self.sets = {times[0]: 0, times[1]: 0}

    def aumentar_pontos(self, time: Time) -> None:
        self.pontos[time] += 1

    def aumentar_sets(self, time: Time) -> None:
        self.sets[time] += 1

    def zerar_pontos(self) -> None:
        for time in self.pontos:
            self.pontos[time] = 0

    def set_em_andamento(self) -> bool:
        """Retorna True se o set não acabou"""
        pontos = list(self.pontos.values())

        if sum(self.sets.values()) < 2 * (self.SETS_PARA_VENCER - 1): # para chegar ao tie break os dois times devem ter um set a menos que o suficiente para vencer
            max_pontos = self.PONTOS_SET
        else:
            max_pontos = self.PONTOS_TIE_BREAK

        return max(pontos) < max_pontos or max(pontos) - min(pontos) < self.VANTAGEM_PARA_VENCER

    def partida_em_andamento(self)  -> bool:
        """Retorna True se a partida não acabou"""
        return max(self.sets.values()) < self.SETS_PARA_VENCER


class Juiz:
    """Classe que define os erros e acertos dos jogadores"""

    LIMIAR_ERRO = 30

    def acertou_jogada(self, qualidade: float) -> bool:
        return qualidade > self.LIMIAR_ERRO


class Partida:
    """Classe que comandará a partida"""

    DESCANSO_TEMPO = 10

    def __init__(self, placar: Placar, juiz: Juiz) -> None:
        self.placar = placar
        self.times = self.placar.times
        self.juiz = juiz

    def tempo(self) -> None:
        for jogador in self.times[0]: 
            jogador.descansar(self.DESCANSO_TEMPO)
        for jogador in self.times[1]: 
            jogador.descansar(self.DESCANSO_TEMPO)

    def jogar_moeda(self) -> int:
        return random.randint(0, 1)

    def disputar_partida(self) -> None:
        indice = self.jogar_moeda()
        time_sacador = self.times[indice]
        time_receptor = self.times[1 - indice]

        while self.placar.partida_em_andamento():
            sacador = time_sacador.escolher_sacador()
            qualidade_saque = sacador.sacar()
            sacador.cansar(1)
            if not self.juiz.acertou_jogada(qualidade_saque):
                self.placar.aumentar_pontos(time_receptor)
            receptor = time_receptor.escolher_receptor()
            qualidade_passe = receptor.receber(qualidade_saque)
            if not self.juiz.acertou_jogada(qualidade_passe):
                self.placar.aumentar_pontos(time_sacador)

            while self.placar.set_em_andamento():
                levantador = time_receptor.escolher_levantador()
                qualidade_levantamento = levantador.levantar(qualidade_passe)
                if not self.juiz.acertou_jogada(qualidade_levantamento):
                    self.placar.aumentar_pontos(time_sacador)
                atacante = time_receptor.escolher_atacante()
                qualidade_ataque = atacante.atacar(qualidade_levantamento)
                atacante.cansar(2)
                if not self.juiz.acertou_jogada(qualidade_ataque):
                    self.placar.aumentar_pontos(time_sacador)
                for jogador in time_receptor.rotacao:
                    jogador.cansar(1)
                for jogador in time_receptor.reservas:
                    jogador.descansar(1)
                bloqueador = time_sacador.escolher_bloqueador()
                qualidade_bloqueio = bloqueador.bloquear(qualidade_ataque)
                bloqueador.cansar(2)
                defensor = time_sacador.escolher_defensor()
                qualidade_passe = defensor.defender(qualidade_ataque, qualidade_bloqueio)
                if not self.juiz.acertou_jogada(qualidade_passe):
                    self.juiz.aumentar_pontos(time_receptor)

            self.placar.zerar_pontos()