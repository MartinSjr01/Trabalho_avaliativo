from modules.interface import Interface
from modules.simulador import Placar, Tecnico, Posicao, Jogador, Time


MAXIMO_NOME_TIME = 20
MAXIMO_NOME_JOGADOR = 15
SIGLAS_ATRIBUTOS = ("ATQ", "PAS", "LEV", "SAQ", "BLO")
funcoes = {
    "levantador": Posicao.LEVANTADOR, "lev": Posicao.LEVANTADOR,
    "oposto" : Posicao.OPOSTO, "opo": Posicao.OPOSTO,
    "ponteiro": Posicao.PONTEIRO, "pon": Posicao.PONTEIRO,
    "central": Posicao.CENTRAL, "cen": Posicao.CENTRAL,
    "libero": Posicao.LIBERO, "lib": Posicao.LIBERO,
    "líbero" : Posicao.LIBERO, "líb": Posicao.LIBERO
}
funcoes_titulares = {
    Posicao.LEVANTADOR: 1,
    Posicao.OPOSTO: 1,
    Posicao.PONTEIRO: 2,
    Posicao.CENTRAL: 2,
    Posicao.LIBERO: 1
}


def mostrar_introducao() -> None:
    """Apresenta o simulador"""
    print(" SIMULADOR DE TÉCNICO DE VÔLEI ".center(Interface.LARGURA_INTERFACE, "="))
    print(
        "-> O simulador de técnico de vôlei depende de como você monta o seu time.\n"
        "-> Você pode pedir:\n"
        f"\t- Tempo (Total de {Tecnico.TEMPOS}).\n"
        f"\t- Substituições (Total de {Tecnico.SUBSTITUICOES}).\n"
        "-> Suas ações interferem e influenciam o jogo!"
    )
    print("=" * Interface.LARGURA_INTERFACE)


def mostrar_regras_basicas() -> None:
    """Relembra as regras básicas do vôlei"""
    print(
        "\n"
        "O jogo é disputado entre 2 times, cada um tem 7 jogadores titulares, 6 em\n"
        "quadra e mais um sétimo que alterna com o líbero ou central. O seu time\n"
        "pontua quando a bola toca no chão da quadra adversária ou uma falta\n"
        "acontece. Faltas ocorrem quando:\n"
        "\t-A bola tocar no time adversário e depois bater no lado de fora da quadra;"
        "\n\t-O time adversário tocar na rede durante um ponto;\n"
        "\t-O time adversário tocar na bola mais de 3 vezes;\n"
        "\t-Durante o saque se o jogador adversário pisar na quadra\n"
        "\n"
        "Os titulares devem ter as seguintes funções:\n"
        "\t-> 1 Levantador: responsável por levantar a bola para os atacantes;\n"
        "\t-> 1 Oposto: responsável por atacar a bola;\n"
        "\t-> 2 Ponteiros: responsáveis por atacar, passar e bloquear;\n"
        "\t-> 2 Centrais: responsáveis por bloquear e atacar;\n"
        "\t-> 1 Líbero: dedicado ao passe (não pode atacar).\n"
    )


def mostrar_informacoes_importantes() -> None:
    """Explica as regras do simulador"""
    sets_total = 2 * Placar.SETS_PARA_VENCER - 1
    sets_empate = Placar.SETS_PARA_VENCER - 1
    print(" INFORMAÇÕES IMPORTANTES ".center(Interface.LARGURA_INTERFACE, "-"))
    print(
        "O técnico pode escolher a posição inicial dos jogadores, fazer substituições"
        "\ne pedir tempo. Um set só acaba quando um time atinge "
        f"{Placar.PONTOS_SET} pontos e a"
        f"\ndiferença entre os pontos é de pelo menos {Placar.VANTAGEM_PARA_VENCER}. "
        f"A partida é melhor de {sets_total} sets,"
        f"\nisto é, é necessário ganhar {Placar.SETS_PARA_VENCER} sets para vencer. "
        f"Caso haja empate em {sets_empate} a {sets_empate},"
        f"\nacontecerá um desempate até {Placar.PONTOS_TIE_BREAK} pontos."
    )
    print("-" * Interface.LARGURA_INTERFACE)

def reg_titulares() -> list[Jogador]:
    """Registra os jogadores titulares"""
    titulares = []
    while len(titulares) < 7:
        nome = input(f"Jogador {len(titulares)+1}: Escreva o nome do jogador: ")
        if len(nome) > MAXIMO_NOME_JOGADOR:
            print(f"O nome do jogador deve ter no máximo {MAXIMO_NOME_JOGADOR} caracteres.")
            continue
        camisa = input(f"Jogador {len(titulares)+1}: Escreva o numero da camisa: ")
        if not camisa.isdigit():
            print("O número da camisa deve ser um número inteiro.")
            continue
        camisa = int(camisa)
        if camisa in [jogador.camisa for jogador in titulares]:
            print("O número da camisa já está em uso. Escolha outro número.")
            continue
        posicao = input(f"Jogador {len(titulares)+1}: Escreva qual a posição do jogador: ")
        posicao = posicao.lower()
        if posicao not in funcoes:  
            print(
                "Posição inválida. Escolha entre levantador (lev), oposto (opo)," 
                " ponteiro (pon), central (cen) ou líbero/libero (líb)/(lib)."
            )
            continue
        posicao = funcoes[posicao]
        quantidade = 0
        for jogador in titulares:
            if jogador.posicao == posicao:
                quantidade += 1
        if quantidade + 1 > funcoes_titulares[posicao]:
            print(f"Você já tem o número máximo de jogadores para a posição {posicao.name}.")
            continue
        ataque = input(f"Jogador {len(titulares)+1}: Escreva a qualidade de ataque: ")
        if not ataque.isdigit():
            print("O ataque deve ser um NÚMERO real.")
            continue
        ataque = int(ataque)
        if not 0 <= ataque <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O ataque tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue  
        passe = input(f"Jogador {len(titulares)+1}: Escreva a qualidade de passe: ")
        if not passe.isdigit():
            print("O passe deve ser um NÚMERO real.")
            continue
        if not 0 <= passe <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O passe tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue 
        levantamento= input(f"Jogador {len(titulares)+1}: Escreva a qualidade de levantamento: ")
        if not passe.isdigit():
            print("O levantamento deve ser um NÚMERO real.")
            continue
        if not 0 <= levantamento <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O levantamento tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue 
        saque = input(f"Jogador {len(titulares)+1}: Escreva a qualidade de saque: ")
        if not saque.isdigit():
            print("O saque deve ser um NÚMERO real.")
            continue
        if not 0 <= saque <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O saque tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue 
        bloqueio = input(f"Jogador {len(titulares)+1}: Escreva a qualidade de bloqueio: ")
        if not bloqueio.isdigit():
                print("O bloqueio deve ser um NÚMERO real.")
                continue
        if not 0 <= bloqueio <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O bloqueio tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue  
        if sum((ataque, passe, levantamento, bloqueio, saque)) > Jogador.MAXIMO_ATRIBUTOS:
            print(f"A soma de todos os atributos tem que ser menor ou igual a {Jogador.MAXIMO_ATRIBUTOS}")
        titulares.append(Jogador(nome, camisa, posicao, ataque, passe, levantamento, saque, bloqueio))
    return titulares

def reg_reservas(
        titulares: list[Jogador]
) -> list[Jogador]:
    """Registra os jogadores reservas"""  
    while True:
        quantidade_reservas = input("Quantos reservas:")
        if not quantidade_reservas.isdigit:
            print("Escreva um numero, não um caracter.")
            continue
        quantidade_reservas = int(quantidade_reservas)
        break
    reservas = []
    while len(reservas) < quantidade_reservas:
        nome = input(f"Jogador {len(reservas)+1}: Escreva o nome do jogador: ")
        if len(nome) > MAXIMO_NOME_JOGADOR:
            print(f"O nome do jogador deve ter no máximo {MAXIMO_NOME_JOGADOR} caracteres.")
            continue
        camisa = input(f"Jogador {len(reservas)+1}: Escreva o numero da camisa: ")
        if not camisa.isdigit():
            print("O número da camisa deve ser um número inteiro.")
            continue
        camisa = int(camisa)
        if camisa in [jogador.camisa for jogador in reservas + titulares]:
            print("O número da camisa já está em uso. Escolha outro número.")
            continue
        posicao = input(f"Jogador {len(reservas)+1}: Escreva qual a posição do jogador: ")
        posicao = posicao.lower()
        if posicao not in funcoes:  
            print(
                "Posição inválida. Escolha entre levantador (lev), oposto (opo)," 
                " ponteiro (pon), central (cen) ou líbero/libero (líb)/(lib)."
            )
            continue
        posicao = funcoes[posicao]
        ataque = input(f"Jogador {len(reservas)+1}: Escreva a qualidade de ataque: ")
        if not ataque.isdigit():
            print("O ataque deve ser um NÚMERO real.")
            continue
        ataque = int(ataque)
        if not 0 <= ataque <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O ataque tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue  
        passe = input(f"Jogador {len(reservas)+1}: Escreva a qualidade de passe: ")
        if not passe.isdigit():
            print("O passe deve ser um NÚMERO real.")
            continue
        if not 0 <= passe <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O passe tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue 
        levantamento= input(f"Jogador {len(reservas)+1}: Escreva a qualidade de levantamento: ")
        if not passe.isdigit():
            print("O levantamento deve ser um NÚMERO real.")
            continue
        if not 0 <= levantamento <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O levantamento tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue 
        saque = input(f"Jogador {len(reservas)+1}: Escreva a qualidade de saque: ")
        if not saque.isdigit():
            print("O saque deve ser um NÚMERO real.")
            continue
        if not 0 <= saque <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O saque tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue 
        bloqueio = input(f"Jogador {len(reservas)+1}: Escreva a qualidade de bloqueio: ")
        if not bloqueio.isdigit():
                print("O bloqueio deve ser um NÚMERO real.")
                continue
        if not 0 <= bloqueio <= Jogador.TAMANHO_ATRIBUTOS:
            print(
                "O bloqueio tem que estar entre 0 a 100, você digitou um numero invávido."
            )
            continue  
        if sum((ataque, passe, levantamento, bloqueio, saque)) > Jogador.MAXIMO_ATRIBUTOS:
            print(f"A soma de todos os atributos tem que ser menor ou igual a {Jogador.MAXIMO_ATRIBUTOS}")
        reservas.append(Jogador(nome, camisa, posicao, ataque, passe, levantamento, saque, bloqueio))
        return reservas

def reg_tecnico() -> Tecnico:
    while True:
        nome_tecnico = input("Escreva seu nome:")
        if nome_tecnico > MAXIMO_NOME_JOGADOR:
            print(
            f"Você extrapolou o número de caracteres!!"
            )
            continue
        return Tecnico(nome_tecnico)

def montar_time() -> Time:
    while True:
        nome_time = input("Escreva o nome do seu time")
        if nome_time > MAXIMO_NOME_JOGADOR:
            print(f"Você passou o número máximo de caracteres")
            continue
        return Time(nome_time, reg_titulares() + reg_reservas(), reg_tecnico())

def main():
    mostrar_introducao()
    mostrar_regras_basicas()
    mostrar_informacoes_importantes()
    
    
#termino do jogo
print(f"O jogo terminou o vencedor foi o {nometime1} com o técnico {tecnico1.nome}" \
      " Agora, gostaríamos de agradecer aos dois jogadores {tecnico1.nome} e {tecnico2.nome} por participarem" \
      " do nosso simulador de técnico de vôlei, esperamos que tenham se divertido e aprendido mais sobre o esporte." \
      " Se quiserem jogar novamente, so clicar em S programa na opção abaixo, caso não queiramm clicam em N." \
explicacao = input("Deseja reiniciar o programa? (S/N): ")
if explicacao.upper() == "S":
    import main
      "Esperamos que após avaliem nosso jogo e deem sugestões de melhorias."
        "CRIADORES: \n -Isabelle Perin \n -Martin Jr \n -Murilo Motta \n -Thomas Ávila")