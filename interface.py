from simulador_tecnico import Jogador, Time


class Interface:
    """Classe que imprimirá textos no terminal"""
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
        saindo = self.perguntar_numero(
            "Escreva o n° da camisa de quem sai", time.em_quadra + [time.setimo]
        )
        entrando = self.perguntar_numero(
            "Escreva o n° da camisa de quem entra", time.reservas
        )
        return (saindo, entrando)