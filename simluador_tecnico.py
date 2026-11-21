import random
from enum import Enum


class Posicao (Enum):
    """Enumeração das posições"""
    LEVANTADOR = 1
    OPOSTO = 2
    PONTEIRO = 3
    CENTRAL = 4
    LIBERO = 5


class AreaAtaque (Enum):
    """Enumeração das regiões em que um ataque pode ser feito"""
    ENTRADA = 1
    MEIO = 2
    SAIDA = 3
    FUNDO = 4


class Jogador:
    """Classe que executa ações"""

    TAMANHO_ATRIBUTOS = 100
    SOMA_ALPHA_BETA = 10
    FATOR_CANSACO = 2 / 3

    def __init__(
            self, nome: str, camisa: int, posicao: Posicao, ataque: float,
            passe: float, levantamento: float, saque: float, bloqueio: float
            ) -> None:
        """Definição de jogador"""
        self.nome = nome
        self.camisa = camisa
        self.posicao = posicao
        self.ataque = ataque
        self.passe = passe
        self.levantamento = levantamento
        self.saque = saque
        self.bloqueio = bloqueio
        self.cansaco = 0

    def _medir_qualidade(self, alpha: float) -> float:
        """Retorna um número pseudo-aleatório a partir da distribuição beta"""
        beta = (self.TAMANHO_ATRIBUTOS - alpha) + self.cansaco * self.FATOR_CANSACO
        alpha_n = max(alpha / self.TAMANHO_ATRIBUTOS * self.SOMA_ALPHA_BETA, 1.2)
        beta_n = max(beta / self.TAMANHO_ATRIBUTOS * self.SOMA_ALPHA_BETA, 1.2)
        return random.betavariate(alpha_n, beta_n) * self.TAMANHO_ATRIBUTOS

    def sacar(self) -> float:
        """Retorna a qualidade do saque do jogador"""
        alpha = self.saque
        return self._medir_qualidade(alpha)

    def receber(self, saque_oponente: float) -> float:
        """Retorna a qualidade da recepção do jogador"""
        alpha = (3 * self.passe + 2 * (self.TAMANHO_ATRIBUTOS - saque_oponente)) / 5
        return self._medir_qualidade(alpha)

    def levantar(self, passe_aliado: float) -> float:
        """Retorna a qualidade do levantamento do jogador"""
        alpha = (3 * self.levantamento + 2 * passe_aliado) / 5
        return self._medir_qualidade(alpha)

    def atacar(self, levantamento_aliado: float) -> float:
        """Retorna a qualidade do ataque do jogador"""
        alpha = (3 * self.ataque + 2 * levantamento_aliado) / 5
        return self._medir_qualidade(alpha)

    def bloquear(self, ataque_oponente: float) -> float:
        """Retorna a qualidade do bloqueio do jogador"""
        alpha = (2 * self.bloqueio + 5 * (self.TAMANHO_ATRIBUTOS - ataque_oponente)) / 7
        return self._medir_qualidade(alpha)

    def defender(self, ataque_oponente: float, bloqueio_aliado: float) -> float:
        """Retorna a qualidade da defesa do jogador"""
        alpha = (3 * self.passe + bloqueio_aliado + 4 * (self.TAMANHO_ATRIBUTOS - ataque_oponente)) / 8
        return self._medir_qualidade(alpha)  

    def cansar(self, valor: int) -> None:
        """Aumenta o cansaço de um jogador"""
        if self.cansaco + valor <= self.TAMANHO_ATRIBUTOS:
            self.cansaco += valor
        else:
            self.cansaco = self.TAMANHO_ATRIBUTOS

    def descansar(self, valor: int) -> None:
        """Diminui o cansaço de um jogador"""
        if self.cansaco - valor >= 0:
            self.cansaco -= valor
        else:
            self.cansaco = 0


class Tecnico:
    """Definição da classe Tecnico"""

    TEMPOS = 2
    SUBSTUICOES = 6

    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.tempos_restantes = self.TEMPOS
        self.substituicoes_restantes = self.SUBSTUICOES
        self.quer_substituir = False
        self.quer_tempo = False

    def pedir_substituicao(self) -> None:
        """Pede para realizar uma substituição"""
        if self.substituicoes_restantes > 0:
            self.quer_substituir = True
            self.substituicoes_restantes -= 1

    def pedir_tempo(self) -> None:
        """Para o jogo por um tempo, descançando os jogadores"""
        if self.tempos_restantes > 0:
            self.quer_tempo = True


class Time:
    """Classe que decide o jogador que executa ações"""

    CONSTANTE_CANSACO = 1
    CONSTANTE_DESCANSO = 1

    def __init__(self, jogadores: list[Jogador], tecnico: Tecnico) -> None:
        """Definição de time"""
        self.jogadores = jogadores
        self.em_quadra = jogadores[:6]
        self.reservas = jogadores[6:]
        self.tecnico = tecnico

    def rodar(self) -> None:
        """Rotaciona os jogadores em quadra"""
        self.em_quadra = self.em_quadra[1:] + self.em_quadra[:1]

    def substituir(self, jogador_entrando: Jogador, jogador_saindo: Jogador) -> None:
        """Troca um jogador do banco por um na quadra"""
        self.em_quadra.replace(jogador_saindo, jogador_entrando)
        self.reservas.replace(jogador_entrando,jogador_saindo)
        self.tecnico.quer_substituir = False

    def escolher_sacador(self) -> Jogador:
        """Retorna o jogador que irá sacar"""
        return self.em_quadra[0]

    def escolher_receptor(self) -> Jogador:
        """Retorna o jogador que irá receber"""
        pesos = {
            Posicao.PONTEIRO: 45,
            Posicao.LIBERO: 50,
            Posicao.OPOSTO: 1.5,
            Posicao.CENTRAL: 3,
            Posicao.LEVANTADOR: 0.5,
        }
        return random.choices(
            self.em_quadra,
            weights=[pesos[j.posicao] for j in self.em_quadra],
            )[0]

    def escolher_levantador(self, passador: Jogador) -> Jogador:
        """Retorna o jogador que irá levantar"""
        pesos = {
            Posicao.PONTEIRO: 6,
            Posicao.LIBERO: 15,
            Posicao.OPOSTO: 1,
            Posicao.CENTRAL: 8,
            Posicao.LEVANTADOR: 70,
            }
        
        possiveis_levantadores = self.em_quadra.remove(passador) #ele escolhe quem vai levantar excluindo quem passou
        
        return random.choices(
            possiveis_levantadores,
            weights=[pesos[j.posicao] for j in self.em_quadra],
            )[0]

    def escolher_atacante(
            self, levantador: Jogador
            ) -> tuple[Jogador, AreaAtaque]:
        """Retorna o jogador que irá atacar e a posição que está na rotação"""
        pesos = {
            Posicao.PONTEIRO: 35,
            Posicao.LIBERO: 0,
            Posicao.OPOSTO: 40,
            Posicao.CENTRAL: 20,
            Posicao.LEVANTADOR: 5,
            }

        possiveis_atacantes = self.em_quadra.remove(levantador) #ele escolhe quem vai atacar excluindo quem levantou
        atacante = random.choices(
            possiveis_atacantes,
            weights=[pesos[j.posicao] for j in self.em_quadra],
            )[0]

        match atacante.posicao:
            case Posicao.LEVANTADOR | Posicao.OPOSTO:
                area_ataque = AreaAtaque.SAIDA
            case Posicao.PONTEIRO:
                if self.em_quadra.index(atacante) in [1, 2, 3]:
                    area_ataque = AreaAtaque.ENTRADA
                else:
                    area_ataque = AreaAtaque.FUNDO
            case Posicao.CENTRAL:
                area_ataque = AreaAtaque.MEIO

        return (atacante, area_ataque)

    def escolher_bloqueadores(
            self, area_ataque: AreaAtaque
            ) -> list[Jogador]:
        """Retorna os jogadores que irão bloquear"""
        match area_ataque:
            case AreaAtaque.ENTRADA | AreaAtaque.MEIO: #saída bloqueia
                return self.em_quadra[1:3]
            case AreaAtaque.SAIDA: #entrada bloqueia
                return self.em_quadra[2:4]
            case AreaAtaque.FUNDO: #todos bloqueiam
                return self.em_quadra[1:4]

    def escolher_defensor(self, bloqueadores: list[Jogador]) -> Jogador:
        """Retorna o jogador que irá defender"""
        pesos = {
            Posicao.PONTEIRO: 25,
            Posicao.LIBERO: 40,
            Posicao.OPOSTO: 16,
            Posicao.CENTRAL: 5,
            Posicao.LEVANTADOR: 14,
            }

        possiveis_defensores = self.em_quadra.remove(bloqueadores) #ele nao deixa o bloqueador defender, e deixa quem nao foi bloquear defender
        
        return random.choices(
            possiveis_defensores,
            weights=[pesos[j.posicao] for j in self.em_quadra],
            )[0]


class Placar:
    """Classe que contabilizará os pontos e sets"""

    PONTOS_SET = 25
    PONTOS_TIE_BREAK = 15
    SETS_PARA_VENCER = 3
    VANTAGEM_PARA_VENCER = 2

    def __init__(self, times: list[Time]) -> None:
        """Definição da de um placar"""
        self.times = times
        self.pontos = {times[0]: 0, times[1]: 0}
        self.sets = {times[0]: 0, times[1]: 0}

    def aumentar_pontos(self, time: Time) -> None:
        """Aumenta em 1 os pontos de um time"""
        self.pontos[time] += 1

    def aumentar_sets(self, time: Time) -> None:
        """Aumenta em 1 os sets de um time"""
        self.sets[time] += 1

    def zerar_pontos(self) -> None:
        """Zera os pontos de ambos times"""
        for time in self.pontos:
            self.pontos[time] = 0

    def set_em_andamento(self) -> bool:
        """Retorna True se o set não acabou"""
        pontos = list(self.pontos.values())

        if sum(self.sets.values()) < 2 * (self.SETS_PARA_VENCER - 1): #para chegar ao tie break os dois times devem ter um set a menos que o suficiente para vencer
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
        """Retorna True se o jogador não errou a jogada"""
        return qualidade > self.LIMIAR_ERRO


class Partida:
    """Classe que comandará a partida"""

    DESCANSO_TEMPO = 10
    CANSACO_PULO = 2

    def __init__(self, placar: Placar, juiz: Juiz) -> None:
        """Definição de partida"""
        self.placar = placar
        self.times = self.placar.times
        self.juiz = juiz

    def tempo(self) -> None:
        """Descança os jogadores quando um técnico pede um tempo"""
        for jogador in self.times[0]:
            jogador.descansar(self.DESCANSO_TEMPO)
        for jogador in self.times[1]:
            jogador.descansar(self.DESCANSO_TEMPO)
        self.times[0].tecnico.quer_tempo = False
        self.times[1].tecnico.quer_tempo = False

    def jogar_moeda(self) -> int:
        """Decide quem começa sacando"""
        return random.randint(0, 1)

    def disputar_partida(self) -> None:
        """Contém o loop que faz a partida acontecer"""
        indice = self.jogar_moeda()
        time_sacador = self.times[indice]
        time_receptor = self.times[1 - indice]

        while self.placar.partida_em_andamento():
            if time_sacador.tecnico.quer_substituir: #interface com player será feita no futuro
                time_sacador.substituir(...) 
            if time_receptor.tecnico.quer_substituir: #interface com player será feita no futuro
                time_receptor.substituir(...)
            if time_sacador.tecnico.quer_tempo:
                self.tempo()
                time_sacador.tecnico.tempos_restantes -= 1
            elif time_receptor.tecnico.quer_tempo:
                self.tempo()
                time_receptor.tecnico.tempos_restantes -= 1
            sacador = time_sacador.escolher_sacador()
            qualidade_saque = sacador.sacar()
            sacador.cansar(self.CANSACO_PULO)
            if not self.juiz.acertou_jogada(qualidade_saque):
                self.placar.aumentar_pontos(time_receptor)
                time_sacador.cansar_jogadores()
                time_receptor.cansar_jogadores()
                time_receptor.rodar()
                continue
            passador = time_receptor.escolher_receptor()
            qualidade_passe = passador.receber(qualidade_saque)
            if not self.juiz.acertou_jogada(qualidade_passe):
                self.placar.aumentar_pontos(time_sacador)
                time_sacador.cansar_jogadores()
                time_receptor.cansar_jogadores()
                continue

            while self.placar.set_em_andamento():
                levantador = time_receptor.escolher_levantador(passador)
                qualidade_levantamento = levantador.levantar(qualidade_passe)
                if not self.juiz.acertou_jogada(qualidade_levantamento):
                    self.placar.aumentar_pontos(time_sacador)
                    time_sacador.cansar_jogadores()
                    time_receptor.cansar_jogadores()
                    break
                atacante, area_ataque = time_receptor.escolher_atacante(levantador)
                qualidade_ataque = atacante.atacar(qualidade_levantamento)
                atacante.cansar(self.CANSACO_PULO)
                if not self.juiz.acertou_jogada(qualidade_ataque):
                    self.placar.aumentar_pontos(time_sacador)
                    time_sacador.cansar_jogadores ()
                    time_receptor.cansar_jogadores()
                    break
                time_sacador.cansar_jogadores()
                time_receptor.cansar_jogadores()
                bloqueadores = time_sacador.escolher_bloqueadores(area_ataque)
                qualidade_bloqueio = 0
                for bloqueador in bloqueadores:
                    qualidade_bloqueio += bloqueador.bloquear(qualidade_ataque)
                qualidade_bloqueio /= len(qualidade_bloqueio)
                bloqueador.cansar(self.CANSACO_PULO)
                passador = time_sacador.escolher_defensor(bloqueadores)
                qualidade_passe = passador.defender(qualidade_ataque, qualidade_bloqueio)
                if not self.juiz.acertou_jogada(qualidade_passe):
                    self.placar.aumentar_pontos(time_receptor)
                    time_sacador.cansar_jogadores()
                    time_receptor.cansar_jogadores()
                    time_receptor.rodar()
                    break
                levantador = time_sacador.escolher_levantador(atacante)
                qualidade_levantamento = levantador.levantar(qualidade_passe)
                if not self.juiz.acertou_jogada(qualidade_levantamento):
                    self.placar.aumentar_pontos(time_receptor)
                    time_sacador.cansar_jogadores()
                    time_receptor.cansar_jogadores()
                    time_receptor.rodar()
                    break
                atacante, area_ataque = time_sacador.escolher_atacante(levantador)
                qualidade_ataque = atacante.atacar(qualidade_levantamento)
                atacante.cansar(self.CANSACO_PULO)
                if not self.juiz.acertou_jogada(qualidade_ataque):
                    self.placar.aumentar_pontos(time_receptor)
                    time_sacador.cansar_jogadores()
                    time_receptor.cansar_jogadores()
                    time_receptor.rodar()
                    break
                time_sacador.cansar_jogadores()
                time_receptor.cansar_jogadores()
                bloqueadores = time_receptor.escolher_bloqueadores(area_ataque)
                qualidade_bloqueio = 0
                for bloqueador in bloqueadores:
                    qualidade_bloqueio += bloqueador.bloquear(qualidade_ataque)
                qualidade_bloqueio /= len(qualidade_bloqueio)
                bloqueador.cansar(self.CANSACO_PULO)
                passador = time_receptor.escolher_defensor(bloqueadores)
                qualidade_passe = passador.defender(qualidade_ataque, qualidade_bloqueio)
                if not self.juiz.acertou_jogada(qualidade_passe):
                    self.placar.aumentar_pontos(time_sacador)
                    time_sacador.cansar_jogadores()
                    time_receptor.cansar_jogadores()
                    break

            self.placar.zerar_pontos()