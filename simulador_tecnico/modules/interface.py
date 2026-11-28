import select
import sys
from time import sleep

from .simulador import Jogador, Placar, Posicao, Tecnico, Time

try:
    import msvcrt
except ImportError:
    msvcrt = None


class Interface:
    """Classe que imprimirá textos no terminal"""

    LARGURA_INTERFACE = 79
    _PAUSA = 1
    _PAUSA_PONTO = 1.5

    def __init__(self) -> None:
        self._frases = {
        "sacar": [
            "errou o saque", "saque fraco", "saque regular",
            "bom saque", "saque excelente",
            ],
        "receber": [
            "errou a recepção", "recepção difícil", "recepção regular",
            "boa recepção", "recepção perfeita",
            ],
        "levantar": [
            "errou o levantamento", "levantamento ruim",
            "levantamento regular", "bom levantamento",
            "levantamento perfeito",
            ],
        "atacar": [
            "errou o ataque", "ataque fraco", "ataque regular",
            "bom ataque", "ataque potente",
            ],
        "defender": [
            "errou a defesa", "defesa apertada", "defesa regular",
            "boa defesa", "defesa espetacular",
            ]
        }
        self._bloqueios = [
            "bloqueio fraco", "bloqueio regular", 
            "bom bloqueio", "bloqueio fechado"
        ]
        self._limites = [40, 60, 80]
        self._formato_time = "{:>3} {:<15}{:<11}{:>8}{:>5}{:>5}{:>5}{:>5}{:>5}"
        self._formato_placar = "{:<2}{:<20}{:>7}{:>6}"
        self._formato_comandos = "{:<15}{:<25}{:<25}{:<15}"

    def _nivel_qualidade(self, qualidade: float) -> int:
        nivel_qualidade = 1
        for limite in self.limites:
            if qualidade >= limite:
                nivel_qualidade += 1
        return nivel_qualidade

    def narrar(
            self, acao : str, jogador: Jogador, qualidade: float, errou: bool
    ) -> None:
        """Narra uma ação"""
        if errou:
            nivel_qld = 0
        else:
            nivel_qld = self.nivel_qualidade(qualidade)
        print(
            f"{jogador.nome} n°: {jogador.camisa}: {self.frases[acao][nivel_qld]}"
        )
        sleep(self.PAUSA)

    def narrar_bloqueio(
            self, bloqueadores: list[Jogador], qualidade: float
            ) -> None:
        """Narra o bloqueio"""
        match len(bloqueadores):
            case 1:
                tipo = "simples"
            case 2:
                tipo = "duplo"
            case 3:
                tipo = "triplo"
        nomes = ", ".join(jogador.nome for jogador in bloqueadores)
        frase = self.bloqueios[self.nivel_qualidade(qualidade) - 1]
        print(f"Bloqueio {tipo} ({nomes}): {frase}")
        sleep(self.PAUSA)

    def mostrar_placar(self, placar: Placar, time_sacador: Time) -> None:
        """Mostra o placar e quem saca"""
        print(f" SET {sum(placar.sets.values()) + 1} ".center(self.LARGURA_INTERFACE, "="))
        print(self.formato_placar.format(
            "", "Time", "Pontos", "Sets")
        .center(self.LARGURA_INTERFACE))
        for time in placar.times:
            if time == time_sacador:
                x = "->"
            else:
                x = ""
            print(self.formato_placar.format(
                x, time.nome, placar.pontos[time], placar.sets[time]
            ).center(self.LARGURA_INTERFACE))
        print("=" * self.LARGURA_INTERFACE)

    def mostrar_ponto(self, time: Time) -> None:
        """Mostra quem fez o ponto"""
        print(f"\n>>> PONTO do {time.nome}!")
        sleep(self.PAUSA_PONTO)

    def mostrar_fim_set(self, placar: Placar, vencedor: Time) -> None:
        """Mostra o resultado do set"""
        perdedor = next(time for time in placar.times if time is not vencedor)
        print(" FIM DO SET ".center(self.LARGURA_INTERFACE, "="))
        print(
            f"{vencedor.nome} vence o set por "
            f"{placar.pontos[vencedor]} a {placar.pontos[perdedor]}!"
            )
        print("=" * self.LARGURA_INTERFACE)
        sleep(self.PAUSA_PONTO)

    def mostrar_fim_partida(self, placar: Placar) -> None:
        """Mostra o vencedor da partida e o placar de sets"""
        sets = max(placar.sets.values())
        vencedor = next(chave for chave, valor in placar.sets.items() if valor == sets)
        print(" FIM DE JOGO ".center(self.LARGURA_INTERFACE, "="))
        print(f"{vencedor.nome} vence a partida! Sets: {sets}")
        print("=" * self.LARGURA_INTERFACE)

    def _linha_tabela(self, jogador: Jogador) -> str:
        """Monta uma linha da tabela que mostra os jogadores"""
        if jogador.posicao is Posicao.LIBERO:
            posicao = "Líbero"
        else:
            posicao = jogador.posicao.name.capitalize()
        linha = self.formato_time.format(
            jogador.camisa, jogador.nome, posicao,
            f"{jogador.cansaco}", f"{jogador.ataque}",
            f"{jogador.passe}", f"{jogador.levantamento}",
            f"{jogador.saque}", f"{jogador.bloqueio}"
        ).center(self.LARGURA_INTERFACE)
        return linha

    def mostrar_time(self, time: Time) -> None:
        """Mostra os jogadores de um time"""
        print(f" {time.nome} ".center(self.LARGURA_INTERFACE, "="))
        print(self.formato_time.format(
            "N°", "Jogador", "Função", "Cansaço", "ATQ", "PAS", "LEV", "SAQ", "BLO"
        ).center(self.LARGURA_INTERFACE))
        print(" Em Quadra ".center(self.LARGURA_INTERFACE, "-"))
        for jogador in time.em_quadra:
            print(self.linha_tabela(jogador))
        print(" Sétimo ".center(self.LARGURA_INTERFACE, "-"))
        print(self.linha_tabela(time.setimo))
        print(" Reservas ".center(self.LARGURA_INTERFACE, "-"))
        for jogador in time.reservas:
            print(self.linha_tabela(jogador))
        print("=" * self.LARGURA_INTERFACE)

    def mostrar_tempo(self, time: Time) -> None:
        """Avisa que um time pediu tempo"""
        print(f"\n>>> TEMPO pedido por {time.nome}! Os jogadores descansam.")
        sleep(self.PAUSA_PONTO)

    def mostrar_substituicao(
            self, time: Time, entrando: Jogador, saindo: Jogador
    ) -> None:
        """Avisa que uma substituição foi feita"""
        print(
            f"\n>>> SUBSTITUIÇÃO no {time.nome}: "
            f"sai {saindo.nome} n°{saindo.camisa}, "
            f"entra {entrando.nome} n°{entrando.camisa}"
        )
        sleep(self.PAUSA_PONTO)

    def _perguntar_numero(self, pergunta: str, jogadores: list[Jogador]) -> Jogador | None:
        """Pergunta o número do jogador que entra/sai; None se o usuário desistir"""
        while True:
            resposta = input(pergunta).strip()
            if resposta == "":
                return None
            try:
                numero = int(resposta)
            except ValueError:
                print("Opção inválida")
                continue
            if numero < 0:
                return None
            for jogador in jogadores:
                if jogador.camisa == numero:
                    return jogador
            print("Opção inválida")

    def perguntar_substituicao(self, time: Time) -> tuple[Jogador, Jogador] | tuple[None, None]:
        """Pergunta e retorna o jogador que entra e o que sai"""
        while True:
            if not time.reservas:
                print("Você não tem reservas")
                return (None, None)
            self.mostrar_time(time)
            saindo = self.perguntar_numero(
                "Escreva o n° da camisa de quem sai (<0 para sair): ", 
                time.em_quadra + [time.setimo]
            )
            if saindo is None:
                return (None, None)
            entrando = self.perguntar_numero(
                "Escreva o n° da camisa de quem entra (<0 para sair): "
                , time.reservas
            )
            if entrando is None:
                return (None, None)
            if entrando.posicao != saindo.posicao:
                print("Os jogadores devem ser da mesma posição")
                continue
            return (entrando, saindo)

    def mostrar_comandos(self, tecnico: Tecnico, placar: Placar) -> None:
        """Mostra as teclas do técnico e quantos pedidos ainda restam"""
        if tecnico == placar.times[0].tecnico:
            tempo, substituicao, informacoes = "1", "2", "3"
        else:
            tempo, substituicao, informacoes = "4", "5", "6"
        print(self.formato_comandos.format(
            f"{tecnico.nome}:",
            f"[{tempo}] pedir tempo ({tecnico.tempos_restantes})",
            f"[{substituicao}] substituir ({tecnico.substituicoes_restantes})",
            f"[{informacoes}] informações"
        ))
    
    def ler_teclas(self) -> list[str]:
        """Retorna as teclas pressionadas sem parar o jogo"""
        teclas = []
        if msvcrt is not None:
            while msvcrt.kbhit():
                teclas.append(msvcrt.getwch().lower())
        elif select.select([sys.stdin], [], [], 0)[0]:
            teclas = list(sys.stdin.readline().strip().lower())
        return teclas