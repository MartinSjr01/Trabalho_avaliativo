from simulador_tecnico import Jogador, Posicao, Time


class Interface:
    """Classe que imprimirá textos no terminal"""

    LARGURA_INTERFACE = 79

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


    def linhha_tabela(self, jogador: Jogador) -> str:
        """Monta uma linha da tabela que mostra os jogadores"""
        if jogador.posicao is Posicao.LIBERO:
            posicao = "Líbero"
        else:
            posicao = jogador.posicao.name.capitalize()
        linha = f"{jogador.camisa:>3} {jogador.nome:<15}{posicao:<11}{jogador.cansaco:>5}{jogador.ataque:>5}{jogador.passe:>5}{jogador.levantamento:>5}{jogador.saque:>5}{jogador.bloqueio:>5}".center(self.LARGURA_INTERFACE)
        return linha

    def mostrar_time(self, time: Time) -> None:
        """Mostra os jogadores de um time"""
        print(f" {time.nome} ".center(self.LARGURA_INTERFACE, "="))
        print(
            f"{'N°':>3} {'Jogador':<15}{'Função':<11}{'Cansaço':>5}{'ATQ':>5}{'PAS':>5}{'LEV':>5}{'SAQ':>5}{'BLO':>5}".center(self.LARGURA_INTERFACE)
        )
        print(" Em Quadra ".center(self.LARGURA_INTERFACE, "-"))
        for jogador in time.em_quadra:
            print(self.linhha_tabela(jogador))
        print(" Sétimo ".center(self.LARGURA_INTERFACE, "-"))
        print(self.linhha_tabela(time.setimo))
        print(" Reservas ".center(self.LARGURA_INTERFACE, "-"))
        for jogador in time.reservas:
            print(self.linhha_tabela(jogador))

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