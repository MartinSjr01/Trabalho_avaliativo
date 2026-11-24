from simulador_tecnico import Jogador, Time


class Interface:
    """Classe que imprimirá textos no terminal"""

    LARGURA_INTERFACE = 79

    def linhha_tabela(self, jogador: Jogador):
        if jogador.posicao is Posicao.LIBERO:
            posicao = "Líbero"
        else:
            posicao = jogador.posicao.name.capitalize()
        linha = f"{jogador.camisa:>3} {jogador.nome:<11}{posicao:<11}{jogador.cansaco:<4}{jogador.ataque:>4}{jogador.passe:>4}{jogador.levantamento:>4}{jogador.saque:>4}{jogador.bloqueio:>4}".center(self.LARGURA_INTERFACE)
        return linha

    def mostrar_time(self, time: Time) -> None:
        """Mostra os jogadores de um time"""
        print(f" {time.nome} ".center(self.LARGURA_INTERFACE, "="))
        print(
            f"{'N°':>3} {'Jogador':<11}{'Função':<11}{'Cansaço':<4}{'ATQ':>4}{'PAS':>4}{'LEV':>4}{'SAQ':>4}{'BLO':>4}".center(self.LARGURA_INTERFACE)
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