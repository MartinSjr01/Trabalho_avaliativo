from modules.interface import Interface
from modules.simulador import Placar, Tecnico


MAXIMO_NOME_TIME = 20
MAXIMO_NOME_JOGADOR = 15
SIGLAS_ATRIBUTOS = ("ATQ", "PAS", "LEV", "SAQ", "BLO")


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


print("Agora que você ja sabe as regras do jogo e como ele funciona vamos começar!")
nome_tecnico1 = input("Tecnico 1: Escreva o seu nome:")
time_tecnico1 = input("Tecnico 1: Escreva o nome do seu time:")
tecnico1 = Tecnico(nome_tecnico1, time_tecnico1)
nome_tecnico2 = input("Tecnico 2: Escreva o seu nome:")
time_tecnico2 = input("Tecnico 2: Escreva o nome do seu time:")
tecnico2 = Tecnico(nome_tecnico2, time_tecnico2)
n = int(input(f"Quantos jogadores o {tecnico1.nome} terá? (mínimo 7 e máximo 16): "))
for i in range(n):
    nome = input(f"Jogador {i+1}: Escreva o nome do jogador: ")
    camisa = input(f"Jogador {i+1}: Escreva o numero da camisa: ")
    posicao = input(f"Jogador {i+1}: Escreva qual a posição do jogador: ") 
    ataque = input(f"Jogador {i+1}: Escreva a qualidade de ataque: ")
    passe = input(f"Jogador {i+1}: Escreva a qualidade de passe: ")
    levantamento= input(f"Jogador {i+1}: Escreva a qualidade de levantamento: ")
    saque = input(f"Jogador {i+1}: Escreva a qualidade de saque: ")
    bloqueio = input(f"Jogador {i+1}: Escreva a qualidade de bloqueio: ")
    alcance = input(f"Jogador {i+1}: Escreva o alcance vertical: ")
m = int(input(f"Quantos jogadores o {tecnico2.nome} terá? (mínimo 7 e máximo 16): "))
for i in range(m):
    nome = input(f"Jogador {i+1}: Escreva o nome do jogador: ")
    camisa = input(f"Jogador {i+1}: Escreva o numero da camisa: ")
    posicao = input(f"Jogador {i+1}: Escreva qual a posição do jogador: ") 
    ataque = input(f"Jogador {i+1}: Escreva a qualidade de ataque: ")
    passe = input(f"Jogador {i+1}: Escreva a qualidade de passe: ")
    levantamento= input(f"Jogador {i+1}: Escreva a qualidade de levantamento: ")
    saque = input(f"Jogador {i+1}: Escreva a qualidade de saque: ")
    bloqueio = input(f"Jogador {i+1}: Escreva a qualidade de bloqueio: ")
    alcance = input(f"Jogador {i+1}: Escreva o alcance vertical: ")
print("Agora que cada ténico já montou seu time, falta vocês darem um nome para eles:")
nometime1 = input(f"Qual será o nome do seu time, {tecnico1.nome}?")
nometime2 = input(f"Qual será o nome do seu time, {tecnico2.nome}?")
print(f"Pronto, agora com os dois times montados, {nometime1} e {nometime2}. vamos jogar!!")
# jogo começa a acontecer aqui

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