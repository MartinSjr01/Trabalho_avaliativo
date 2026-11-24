from time import sleep

from simulador_tecnico import Jogador, Placar, Posicao, Time


class Interface:
    """Classe que imprimirá textos no terminal"""

    LARGURA_INTERFACE = 79
    PAUSA = 1
    PAUSA_PONTO = 1.5

    def __init__(self):
        self.frases = {
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
        self.limites = [40, 60, 80]
        self.formato_time = "{:>3} {:<15}{:<11}{:>5}{:>5}{:>5}{:>5}{:>5}{:>5}"
        self.formato_placar = "{:<2}{:<20}{:>7}{:>6}"

    def narrar(
            self, acao : str, jogador: Jogador, qualidade: float, errou: bool
    ) -> None:
        """Narra uma ação"""
        if errou:
            nivel_qualidade = 0
        else:
            nivel_qualidade = 1
            for limite in self.limites:
                if qualidade >= limite:
                    nivel_qualidade += 1
        print(
            f"{jogador.nome} n°: {jogador.camisa}: {self.frases[acao][nivel_qualidade]}"
        )
        sleep(self.PAUSA)

    def mostrar_placar(self, placar: Placar, time_sacador: Time) -> None:
        """Mostra o placar e quem saca"""
        print(f" SET {sum(placar.sets.values()) + 1} ".center(self.LARGURA_INTERFACE))
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
        print("=" * self.LARGURA)

    def mostrar_ponto(self, time: Time) -> None:
        """Mostra quem fez o ponto"""
        print(f"\n>>> PONTO do {time.nome}!")
        self.pausa(self.PAUSA_PONTO)

    def mostrar_fim_set(self, placar: Placar, vencedor: Time) -> None:
        """Mostra o resultado do set"""
        perdedor = (time for time in placar.times if time is not vencedor)
        print(" FIM DO SET ".center(self.LARGURA, "="))
        print(
            f"{vencedor.nome} vence o set por "
            f"{placar.pontos[vencedor]} a {placar.pontos[perdedor]}!"
            )
        print("=" * self.LARGURA)
        sleep(self.PAUSA_PONTO)

    def mostrar_fim_partida(self, placar: Placar) -> None:
        """Mostra o vencedor da partida e o placar de sets"""
        sets = max(placar.sets.values())
        vencedor = (chave for chave, valor in placar.sets.items() if valor == sets)
        print(" FIM DE JOGO ".center(self.LARGURA, "="))
        print(f"{vencedor.nome} vence a partida! Sets: {sets}")
        print("=" * self.LARGURA)

    def linhha_tabela(self, jogador: Jogador) -> str:
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
            print(self.linhha_tabela(jogador))
        print(" Sétimo ".center(self.LARGURA_INTERFACE, "-"))
        print(self.linhha_tabela(time.setimo))
        print(" Reservas ".center(self.LARGURA_INTERFACE, "-"))
        for jogador in time.reservas:
            print(self.linhha_tabela(jogador))
        print("=" * self.LARGURA)

    def perguntar_numero(self, pergunta: str, jogadores: list[Jogador]) -> Jogador:
        """Pergunta o número do jogador que entra/sai"""
        while True:
            resposta = int(input(f"{pergunta}"))
            for jogador in jogadores:
                if resposta == jogador.camisa:
                    return jogador
            print("Opção inválida")

    def perguntar_substituicao(self, time: Time) -> tuple[Jogador, Jogador]:
        """Pergunta e retorna o jogador que entra e o que sai"""
        self.mostrar_time(time)
        saindo = self.perguntar_numero(
            "Escreva o n° da camisa de quem sai", time.em_quadra + [time.setimo]
        )
        entrando = self.perguntar_numero(
            "Escreva o n° da camisa de quem entra", time.reservas
        )
        return (saindo, entrando)