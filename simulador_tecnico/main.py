from time import sleep

from modules.interface import Interface
from modules.simulador import Jogador, Partida, Placar, Posicao, Tecnico, Time

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

def perguntar_sim_nao(pergunta: str) -> bool:
    """Repete a pergunta até receber uma resposta de sim ou não"""
    while True:
        resposta = input(pergunta).strip().lower()
        if resposta in ("s", "sim", "y", "yes"):
            return True
        if resposta in ("n", "não", "nao", "no"):
            return False
        print("Opção inválida")

def ler_string(texto: str, maximo_char: int) -> str:
    """Retorna uma string escrita pelo usuário"""
    while True:
        str = input(texto)
        if len(str) > maximo_char:
            print(f"Deve ter no máximo {maximo_char} carácteres")
            continue
        return str

def ler_numero(
        texto: str, minimo: float, maximo: float, inteiro: bool
) -> int | float:
    """Retorna um número escrito pelo usuário"""
    while True:
        numero = input(texto)
        if inteiro:
            try:
                numero = int(numero)
            except ValueError:
                print("Digite um NÚMERO inteiro")
                continue
        else:
            try:
                numero = float(numero)
            except ValueError:
                print("Digite um NÚMERO real.")
                continue
        if not minimo <= numero <= maximo:
            print(f"O número deve estar no intervalo [{minimo}, {maximo}]")
            continue
        return numero

def mostrar_introducao() -> None:
    """Apresenta o simulador"""
    print(
        " SIMULADOR DE TÉCNICO DE VÔLEI ".center(Interface.LARGURA_INTERFACE, "=")
    )
    print(
        "-> O simulador de técnico de vôlei depende de como você monta o seu "
        "time.\n"
        "-> Você pode pedir:\n"
        f"\t- Tempo (Total de {Tecnico.TEMPOS}).\n"
        f"\t- Substituições (Total de {Tecnico.SUBSTITUICOES}).\n"
        "-> Suas ações interferem no jogo!"
    )
    print("=" * Interface.LARGURA_INTERFACE)

def mostrar_regras_basicas() -> None:
    """Relembra as regras básicas do vôlei"""
    print(
        "\n"
        "O jogo é disputado entre 2 times, cada um tem 7 jogadores "
        "titulares, 6 em\n"
        "quadra e mais um sétimo que alterna com o líbero ou central. O seu "
        "time pontua\n"
        "quando a bola toca no chão da quadra adversária ou uma falta "
        "acontece. Faltas\n"
        "ocorrem quando:\n"
        "\t-A bola tocar no time adversário e depois bater no lado de fora "
        "da\n"
        "\t quadra;\n"
        "\t-O time adversário tocar na rede durante um ponto;\n"
        "\t-O time adversário tocar na bola mais de 3 vezes;\n"
        "\t-Durante o saque se o jogador adversário pisar na quadra\n"
        "\n"
        "Os titulares devem ter as seguintes funções:\n"
        "\t-> 1 Levantador: responsável por levantar a bola para os "
        "atacantes;\n"
        "\t-> 1 Oposto: responsável por atacar a bola;\n"
        "\t-> 2 Ponteiros: responsáveis por atacar, passar e bloquear;\n"
        "\t-> 2 Centrais: responsáveis por bloquear e atacar;\n"
        "\t-> 1 Líbero: dedicado ao passe (não pode atacar).\n"
    )
    input("Enter para continuar: ")

def mostrar_informacoes_importantes() -> None:
    """Explica as regras do simulador"""
    sets_total = 2 * Placar.SETS_PARA_VENCER - 1
    sets_empate = Placar.SETS_PARA_VENCER - 1
    print(
        " INFORMAÇÕES IMPORTANTES ".center(Interface.LARGURA_INTERFACE, "-")
    )
    print(
        "O técnico pode escolher a posição inicial dos jogadores, fazer "
        "substituições e\n"
        "pedir tempo. Um set só acaba quando um time atinge "
        f"{Placar.PONTOS_SET} pontos e a diferença\n"
        f"entre os pontos é de pelo menos {Placar.VANTAGEM_PARA_VENCER}. A "
        f"partida é melhor de {sets_total} sets, isto é, é\n"
        f"necessário ganhar {Placar.SETS_PARA_VENCER} sets para vencer. Caso "
        f"haja empate em {sets_empate} a {sets_empate}, acontecerá um\n"
        f"desempate até {Placar.PONTOS_TIE_BREAK} pontos."
    )
    print("-" * Interface.LARGURA_INTERFACE)

def reg_jogador(jogadores: list[Jogador], titular: bool) -> Jogador:
    """Monta um jogador com todas suas carácterísticas"""
    nome = ler_string("Escreva o nome do jogador: ", MAXIMO_NOME_JOGADOR)
    while True:
        camisa = ler_numero("Escreva o numero da camisa do jogador: ", 0, 999, True)
        if camisa in [jogador.camisa for jogador in jogadores]:
            print("O número da camisa já está em uso. Escolha outro número.")
            continue
        break
    while True:
        posicao = input("Escreva qual a posição do jogador: ").strip().lower()
        if posicao not in funcoes:
            print(
                "Posição inválida. Escolha entre levantador (lev), oposto (opo),"
                " ponteiro (pon),\ncentral (cen) ou líbero/libero (líb)/(lib)."
            )
            continue
        posicao = funcoes[posicao]
        if titular:
            quantidade = sum(1 for jogador in jogadores if jogador.posicao == posicao)
            if quantidade + 1 > funcoes_titulares[posicao]:
                print(
                    "Você já tem o número máximo de jogadores para a posição"
                    f"{posicao.name.lower()}."
                )
                continue
        break
    while True:
        ataque = ler_numero(
            "Escreva a habilidade de ataque do jogador: ",
            0, Jogador.TAMANHO_ATRIBUTOS,False
        )
        passe = ler_numero(
            "Escreva a habilidade de passe do jogador: ",
            0, Jogador.TAMANHO_ATRIBUTOS,False
        )
        levantamento = ler_numero(
            "Escreva a habilidade de levantamento do jogador: ",
            0, Jogador.TAMANHO_ATRIBUTOS,False
        )
        saque = ler_numero(
            "Escreva a habilidade de saque do jogador: ",
            0, Jogador.TAMANHO_ATRIBUTOS,False
        )
        bloqueio = ler_numero(
            "Escreva a habilidade de bloqueio do jogador: ",
            0, Jogador.TAMANHO_ATRIBUTOS,False
        )
        passou_maximo = sum(
            (ataque, passe, levantamento, bloqueio, saque)
        ) > Jogador.MAXIMO_ATRIBUTOS
        if passou_maximo:
            print(
                f"A soma de todos os atributos tem que ser <= {Jogador.MAXIMO_ATRIBUTOS}"
            )
            continue
        break
    print("Jogador registrado. Próximo...\n")
    sleep(1)
    return Jogador(nome, camisa, posicao, ataque, passe, levantamento, saque, bloqueio)

def reg_titulares() -> list[Jogador]:
    """Registra os jogadores titulares"""
    print(" TITULARES ".center(Interface.LARGURA_INTERFACE, "-"))
    titulares = []
    while len(titulares) < Time.MINIMO_JOGADORES:
        titulares.append(reg_jogador(titulares, True))
    return titulares

def reg_reservas(titulares: list[Jogador]) -> list[Jogador]:
    """Registra os jogadores reservas"""  
    print(" RESERVAS ".center(Interface.LARGURA_INTERFACE, "-"))
    quantidade_reservas = ler_numero(
        "Escreva quantos reservas seu time terá (0, caso nenhum e no máximo "
        f"{Time.MAXIMO_JOGADORES})"
    )
    reservas = []
    while len(reservas) < quantidade_reservas:
        reservas.append(reg_jogador(titulares + reservas, False))
    return reservas

def organizar_jogadores(
        titulares: list[Jogador], reservas: list[Jogador]
) -> list[Jogador]:
    """Organiza os titulares no formato 5x1 e retorna:
    [titulares] + [sétimo] + [reservas]"""
    organizados = []
    for i in range(len(Time.posicionamento_base)):
        organizados.append(next(
            jogador for jogador in titulares 
            if jogador.posicao == Time.posicionamento_base[i]
            and jogador not in organizados 
        ))
    posicao_inicial = ler_numero("Posição inicial do levantador: ", 1, 6, True) - 1
    organizados = organizados[-posicao_inicial:] + organizados[:-posicao_inicial]
    setimo = next(
        jogador for jogador in titulares if jogador.posicao == Posicao.LIBERO
    )
    return organizados + [setimo] + reservas

def montar_time() -> Time:
    nome_time = ler_string("Digite o nome do seu time: ", MAXIMO_NOME_TIME)
    nome_tecnico = ler_string("Digite o seu nome: ", MAXIMO_NOME_JOGADOR)
    print(
        "Agora você digitará as características de cada jogador.\n"
        f"-> Cada atributo vai de 0 a {Jogador.TAMANHO_ATRIBUTOS} e a soma dos 5 "
        f"não pode passar de {Jogador.MAXIMO_ATRIBUTOS}.\n"
        "-> Posição: levantador, oposto, ponteiro, central ou líbero (ou lev, opo, "
        "pon,\n   cen, líb).\n"
        f"-> Titulares ({Time.MINIMO_JOGADORES}): 1 levantador, 1 oposto, 2 ponteiros"
        ", 2 centrais e 1 líbero,\n   em qualquer ordem.\n"
    )
    titulares = reg_titulares()
    reservas = reg_reservas(titulares)
    jogadores = organizar_jogadores(titulares + reservas)
    return Time(nome_time, jogadores, nome_tecnico)

def criar_times_genéricos() -> tuple[Time]:
    time_1 = Time(
        "Tigres",
        [
            Jogador("Bruno", 1, Posicao.LEVANTADOR, 40, 60, 100, 55, 40),
            Jogador("Marina", 9, Posicao.PONTEIRO, 90, 70, 20, 65, 45),
            Jogador("Camila", 12, Posicao.CENTRAL, 70, 30, 15, 50, 100),
            Jogador("Rafael", 10, Posicao.OPOSTO, 100, 40, 10, 80, 65),
            Jogador("Thiago", 7, Posicao.PONTEIRO, 85, 80, 10, 60, 50),
            Jogador("Beatriz", 14, Posicao.CENTRAL, 75, 35, 5, 55, 95),
            Jogador("Carolina", 3, Posicao.LIBERO, 5, 100, 100, 5, 5),
            Jogador("André", 11, Posicao.PONTEIRO, 80, 65, 20, 60, 45),
            Jogador("Felipe", 15, Posicao.CENTRAL, 65, 30, 15, 50, 90),
        ],
        Tecnico("Larissa")
    )
    time_2 = Time(
        "Falcões",
        [
            Jogador("Fernanda", 2, Posicao.LEVANTADOR, 45, 55, 95, 60, 40),
            Jogador("Leandro", 8, Posicao.PONTEIRO, 88, 75, 20, 62, 45),
            Jogador("Juliana", 13, Posicao.CENTRAL, 72, 30, 5, 58, 98),
            Jogador("Vitor", 11, Posicao.OPOSTO, 98, 40, 10, 82, 55),
            Jogador("Leticia", 6, Posicao.PONTEIRO, 82, 82, 10, 68, 50),
            Jogador("Patricia", 15, Posicao.CENTRAL, 70, 35, 15, 50, 95),
            Jogador("Samuel", 4, Posicao.LIBERO, 5, 100, 100, 5, 5),
            Jogador("Otávio", 17, Posicao.PONTEIRO, 78, 68, 20, 60, 45),
            Jogador("Amanda", 18, Posicao.CENTRAL, 62, 30, 15, 52, 88),
        ],
        Tecnico("Roberto")
    )
    return (time_1, time_2)

def main() -> None:
    mostrar_introducao()
    if perguntar_sim_nao("Deseja relembrar algumas regras do vôlei? "):
        mostrar_regras_basicas()
    mostrar_informacoes_importantes()
    if perguntar_sim_nao("Deseja utilizar times de exemplo? "):
        time1, time2 = criar_times_genéricos()
    else:
        print(" TIME 1 ".center(Interface.LARGURA_INTERFACE, "-"))
        time1 = montar_time()
        print(" TIME 2 ".center(Interface.LARGURA_INTERFACE, "-"))
        time2 = montar_time()
    partida = Partida(Placar([time1, time2]), Interface())
    partida.disputar_partida()

if __name__ == "__main__":
    main()