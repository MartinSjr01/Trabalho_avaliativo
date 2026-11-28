from __future__ import annotations

import random
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface import Interface


class Posicao(Enum):
    """Enumeração das posições"""
    LEVANTADOR = 1
    OPOSTO = 2
    PONTEIRO = 3
    CENTRAL = 4
    LIBERO = 5


class AreaAtaque(Enum):
    """Enumeração das regiões em que um ataque pode ser feito"""
    ENTRADA = 1
    MEIO = 2
    SAIDA = 3
    FUNDO = 4


class Jogador:
    """Classe que executa ações"""

    _FATOR_CANSACO = 2 / 3
    MAXIMO_ATRIBUTOS = 300
    _SOMA_ALPHA_BETA = 10
    TAMANHO_ATRIBUTOS = 100

    def __init__(
            self, nome: str, camisa:  int, posicao: Posicao, ataque: float,
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
        # tratamento de erros
        total = (
            self.ataque + self.passe + self.levantamento + self.saque + self.bloqueio
        )
        if  not 0 <= total <= self.MAXIMO_ATRIBUTOS:
            raise ValueError(
                f"O jogador {self.nome} tem que possuir entre [0, {self.MAXIMO_ATRIBUTOS}] atributos"
            )
        if self.camisa < 0:
            raise ValueError(
                f"(O jogador {self.nome} tem um número de camisa negativo)"
            )

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
    SUBSTITUICOES = 6

    def __init__(self, nome: str) -> None:
        """Definição da classe técnico"""
        self.nome = nome
        self.tempos_restantes = self.TEMPOS
        self.substituicoes_restantes = self.SUBSTITUICOES
        self.quer_substituir = False
        self.quer_tempo = False

    def pedir_substituicao(self) -> None:
        """Pede para realizar uma substituição"""
        if self.substituicoes_restantes > 0:
            self.quer_substituir = True

    def pedir_tempo(self) -> None:
        """Para o jogo por um tempo, descansando os jogadores"""
        if self.tempos_restantes > 0:
            self.quer_tempo = True


class Time:
    """Classe que decide o jogador que executa ações"""

    MAXIMO_JOGADORES = 12
    MINIMO_JOGADORES = 7
    # posicionamento das funções com o levantador na 1; colocado fora do __init__
    # pois preciso utilizar antes de criar um time no main
    posicionamento_base = [  # noqa: RUF012
        Posicao.LEVANTADOR, Posicao.PONTEIRO, Posicao.CENTRAL,
        Posicao.OPOSTO, Posicao.PONTEIRO, Posicao.CENTRAL
    ]

    def __init__(
            self, nome: str, jogadores: list[Jogador], tecnico: Tecnico
    ) -> None:
        """Definição de time"""
        self.nome = nome
        self.jogadores = jogadores
        # tratamento de erros
        if len(self.jogadores) > self.MAXIMO_JOGADORES or len(self.jogadores) < self.MINIMO_JOGADORES:
            raise ValueError(
                f"O time {self.nome} não tem entre [{self.MINIMO_JOGADORES}, {self.MAXIMO_JOGADORES}] jogadores"
            )
        camisas = [jogador.camisa for jogador in self.jogadores]
        for camisa in camisas:
            if camisas.count(camisa) > 1:
                raise ValueError(
                    f"O time {self.nome} tem camisas repetidas"
                )
        self.em_quadra = jogadores[:6]
        self.setimo = jogadores[6]
        self.reservas = jogadores[7:]
        self.tecnico = tecnico
        # tratamento de erros
        for i in range(6):
            x = self.em_quadra[i:] + self.em_quadra[:i]
            if x[0].posicao is not Posicao.LEVANTADOR:
                continue
            for j in range(6):
                esperado = self.posicionamento_base[j]
                posicao = x[j].posicao
                libero_valido = (
                    posicao is Posicao.LIBERO
                    and esperado is Posicao.CENTRAL
                    and (i + j) % 6 in (0, 4, 5)
                )
                if posicao is not esperado and not libero_valido:
                    raise ValueError(
                        f"A ordem das posições do time {self.nome} não está no padrão da 5x1"
                    )
            break
        else:
            raise ValueError(f"O time {self.nome} não tem levantador em quadra")
        if self.setimo.posicao not in (Posicao.CENTRAL, Posicao.LIBERO):
            raise ValueError(
                f"O sétimo do time {self.nome} não é nem central nem líbero"
            )
        else:
            for jogador in [self.em_quadra[0], self.em_quadra[4], self.em_quadra[5]]:
                if (jogador.posicao == self.setimo.posicao):
                    raise ValueError(
                        f"Tem um {jogador.posicao} no fundo e o sétimo também é"
                    )

    def rodar(self) -> None:
        """Rotaciona os jogadores em quadra"""
        self.em_quadra = self.em_quadra[1:] + self.em_quadra[:1]

    def entra_libero(self):
        """Faz a troca do líbero com o central"""
        for jogador in [self.em_quadra[0], self.em_quadra[4], self.em_quadra[5]]:
            if jogador.posicao is Posicao.CENTRAL:
                self.em_quadra[self.em_quadra.index(jogador)] = self.setimo
                self.setimo = jogador
                break

    def entra_central(self):
        """Quando o líbero está na rede troca com o central"""
        for jogador in self.em_quadra[1:4]:
            if jogador.posicao is Posicao.LIBERO:
                self.em_quadra[self.em_quadra.index(jogador)] = self.setimo
                self.setimo = jogador
                break

    def substituir(
            self, jogador_entrando: Jogador, jogador_saindo: Jogador
    ) -> None:
        """Troca um jogador do banco por um na quadra"""
        titulares = self.em_quadra + [self.setimo]
        i = titulares.index(jogador_saindo)
        j = self.reservas.index(jogador_entrando)
        titulares[i], self.reservas[j] = jogador_entrando, jogador_saindo
        self.em_quadra, self.setimo = titulares[:6], titulares[6]
        self.tecnico.substituicoes_restantes -= 1
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
        possiveis_levantadores = [
            jogador for jogador in self.em_quadra if jogador is not passador
        ] # ele escolhe quem vai levantar excluindo quem passou
        return random.choices(
            possiveis_levantadores,
            weights=[pesos[j.posicao] for j in possiveis_levantadores],
        )[0]

    def escolher_atacante(
            self, levantador: Jogador
    ) -> tuple[Jogador, AreaAtaque]:
        """Retorna o jogador que irá atacar e área de onde ataca"""
        pesos = {
            Posicao.PONTEIRO: 35,
            Posicao.LIBERO: 0,
            Posicao.OPOSTO: 40,
            Posicao.CENTRAL: 20,
            Posicao.LEVANTADOR: 5,
        }
        possiveis_atacantes = [
            jogador for jogador in self.em_quadra if jogador is not levantador
        ] # ele escolhe quem vai atacar excluindo quem levantou
        atacante = random.choices(
            possiveis_atacantes,
            weights=[pesos[j.posicao] for j in possiveis_atacantes],
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
            case AreaAtaque.ENTRADA | AreaAtaque.MEIO: # saída bloqueia
                return self.em_quadra[1:3]
            case AreaAtaque.SAIDA: # entrada bloqueia
                return self.em_quadra[2:4]
            case AreaAtaque.FUNDO: # todos bloqueiam
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
        possiveis_defensores = [
            jogador for jogador in self.em_quadra if jogador not in bloqueadores
        ] # ele nao deixa o bloqueador defender, e deixa quem nao foi bloquear defender
        return random.choices(
            possiveis_defensores,
            weights=[pesos[j.posicao] for j in possiveis_defensores],
        )[0]


class Placar:
    """Classe que contabilizará os pontos e sets"""

    PONTOS_SET = 25
    PONTOS_TIE_BREAK = 15
    SETS_PARA_VENCER = 3
    VANTAGEM_PARA_VENCER = 2

    def __init__(self, times: list[Time]) -> None:
        """Definição de um placar"""
        self.times = times
        # tratamento de erros
        if len(self.times) != 2:
            raise ValueError(
                "Não foram criados 2 times para participar da partida"
            )
        if self.times[0] == self.times[1]:
            raise ValueError(
                "Os dois times são iguais"
            )
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
        if sum(self.sets.values()) < 2 * (self.SETS_PARA_VENCER - 1): # para chegar ao tie break os dois times devem ter um set a menos que o suficiente para vencer
            max_pontos = self.PONTOS_SET
        else:
            max_pontos = self.PONTOS_TIE_BREAK
        nao_max = max(pontos) < max_pontos
        nao_vantagem = max(pontos) - min(pontos) < self.VANTAGEM_PARA_VENCER
        return nao_max or nao_vantagem

    def partida_em_andamento(self) -> bool:
        """Retorna True se a partida não acabou"""
        return max(self.sets.values()) < self.SETS_PARA_VENCER


class Partida:
    """Classe que comandará a partida"""

    _CANSACO_PULO = 1.5
    _CONSTANTE_CANSACO = 0.75
    _CONSTANTE_DESCANSO = 1
    _DESCANSO_TEMPO = 20
    _LIMIAR_ERRO = 30

    def __init__(self, placar: Placar, interface: Interface) -> None:
        """Definição de partida"""
        self.placar = placar
        self.interface = interface
        self.times = self.placar.times
        self.time_sacador = self.times[self.jogar_moeda()]
        self.primeiro_sacador = self.time_sacador
        self.time_atacante = None
        self.time_defensor = None
        self.organizar_time_atacante()
        self._comandos = {
            "1": [0, "tempo"], "2": [0, "substituicao"], "3": [0, "informacoes"],
            "4": [1, "tempo"], "5": [1, "substituicao"], "6": [1, "informacoes"],
        }

    def _tempo(self) -> None:
        """Descansa os jogadores quando um técnico pede um tempo"""
        for jogador in self.times[0].em_quadra + self.times[1].em_quadra:
            jogador.descansar(self.DESCANSO_TEMPO)
        self.times[0].tecnico.quer_tempo = False
        self.times[1].tecnico.quer_tempo = False

    def _conferir_teclas(self) -> None:
        """Executa os comandos que precisam de teclas"""
        for tecla in self.interface.ler_teclas():
            if tecla not in self.comandos:
                continue
            indice, acao = self.comandos[tecla][0], self.comandos[tecla][1]
            match acao:
                case "tempo":
                    self.times[indice].tecnico.pedir_tempo()
                case "substituicao":
                    self.times[indice].tecnico.pedir_substituicao()
                case "informacoes":
                    self.interface.mostrar_time(self.times[indice])
                    input("Enter para retomar: ")

    def _atender_pedidos(self) -> None:
        """Verifica se os tecnicos pedem alguma ação"""
        indice = self.jogar_moeda() # para escolher aleatóriamente qual técnico vai pedir tempo primeiro
        for i in (indice, 1 - indice):
            if self.times[i].tecnico.quer_tempo:
                self.interface.mostrar_tempo(self.times[i])
                self.tempo()
                self.times[i].tecnico.tempos_restantes -= 1
        for time in self.times:
            if time.tecnico.quer_substituir:
                entrando, saindo = self.interface.perguntar_substituicao(time)
                if None not in (entrando, saindo):
                    time.substituir(entrando, saindo)
                    self.interface.mostrar_substituicao(time, entrando, saindo)
                else:
                    time.tecnico.quer_substituir = False 

    def _atualizar_cansaco(self) -> None:
        """Cansa os jogadores em quadra e descansa o sétimo e reservas"""
        for time in self.times:
            for jogador in time.em_quadra:
                jogador.cansar(self.CONSTANTE_CANSACO)
            for jogador in time.reservas + [time.setimo]:
                jogador.descansar(self.CONSTANTE_DESCANSO)

    def _errou_jogada(self, acao: str, jogador: Jogador, qualidade: float) -> bool:
        """Narra a jogada e retorna True se o jogador errou"""
        errou = qualidade < self.LIMIAR_ERRO
        self.interface.narrar(acao, jogador, qualidade, errou)
        return errou

    def _jogar_moeda(self) -> int:
        """Decide quem começa sacando"""
        return random.randint(0, 1)

    def _organizar_time_atacante(self) -> None:
        """Define qual time está com a bola (atacante) e qual não está (defensor)"""
        for time in self.times:
            if time == self.time_sacador:
                self.time_defensor = time
            else:
                self.time_atacante = time

    def _aconteceu_ponto(self, time_pontuou: Time) -> None:
        """Faz tudo que tem que acontecer após um ponto"""
        self.placar.aumentar_pontos(time_pontuou)
        self.interface.mostrar_ponto(time_pontuou)
        self.atualizar_cansaco()

        if time_pontuou != self.time_sacador:
            time_pontuou.rodar()
            if self.time_sacador.em_quadra[0].posicao is Posicao.CENTRAL:
                self.time_sacador.entra_libero()
            if time_pontuou.em_quadra[0].posicao is not Posicao.CENTRAL:
                time_pontuou.entra_libero()
            else:
                time_pontuou.entra_central()
            self.time_sacador = time_pontuou

        if not self.placar.set_em_andamento():
            self.interface.mostrar_fim_set(self.placar, time_pontuou)
            self.placar.aumentar_sets(time_pontuou)
            self.primeiro_sacador = next(
                time for time in self.times if time is not self.primeiro_sacador
            )
            self.time_sacador = self.primeiro_sacador
            self.placar.zerar_pontos()

    def _disputar_rally(self, qualidade_saque: float) -> None:
        """Loop que faz um rally acontecer, é sempore o time defensor que pontua"""
        is_saque = True
        bloqueadores, qualidade_ataque, qualidade_bloqueio = None, None, None
        while True:
            if is_saque:
                passador = self.time_atacante.escolher_receptor()
                qualidade_passe = passador.receber(qualidade_saque)
                acao = "receber"
                is_saque = False
            else:
                passador = self.time_atacante.escolher_defensor(bloqueadores)
                qualidade_passe = passador.defender(qualidade_ataque, qualidade_bloqueio)
                acao = "defender"
            if self.errou_jogada(acao, passador, qualidade_passe):
                return
            levantador = self.time_atacante.escolher_levantador(passador)
            qualidade_levantamento = levantador.levantar(qualidade_passe)
            if self.errou_jogada("levantar", levantador, qualidade_levantamento):
                return
            atacante, area_ataque = self.time_atacante.escolher_atacante(levantador)
            qualidade_ataque = atacante.atacar(qualidade_levantamento)
            atacante.cansar(self.CANSACO_PULO)
            if self.errou_jogada("atacar", atacante, qualidade_ataque):
                return
            self.atualizar_cansaco()
            bloqueadores = self.time_defensor.escolher_bloqueadores(area_ataque)
            qualidade_bloqueio = 0
            for bloqueador in bloqueadores:
                qualidade_bloqueio += bloqueador.bloquear(qualidade_ataque)
                bloqueador.cansar(self.CANSACO_PULO)
            qualidade_bloqueio /= len(bloqueadores)
            self.interface.narrar_bloqueio(bloqueadores, qualidade_bloqueio)
            self.time_atacante, self.time_defensor = self.time_defensor, self.time_atacante

    def _disputar_ponto(self) -> None:
        """Realiza o saque e chama disputar_rally()"""
        self.organizar_time_atacante()
        sacador = self.time_sacador.escolher_sacador()
        qualidade_saque = sacador.sacar()
        sacador.cansar(self.CANSACO_PULO)
        if self.errou_jogada("sacar", sacador, qualidade_saque):
            self.aconteceu_ponto(self.time_atacante)
            return
        self.disputar_rally(qualidade_saque)
        self.aconteceu_ponto(self.time_defensor)

    def disputar_partida(self) -> None:
        """Contém o loop que faz a partida acontecer"""
        while self.placar.partida_em_andamento():
            self.interface.mostrar_placar(self.placar, self.time_sacador)
            for time in self.times:
                self.interface.mostrar_comandos(time.tecnico, self.placar)
                time.entra_central()
                time.entra_libero()
            self.disputar_ponto()
            if not self.placar.partida_em_andamento():
                break
            self.conferir_teclas()
            self.atender_pedidos()
        self.interface.mostrar_fim_partida(self.placar)