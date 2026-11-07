
from simulador_tecnico import *
"""EXPLICAÇÃO DO JOGO"""
print("O simulador de técnico de vôlei é passeado em como você montaria o seu time e iria lidar com as consequências de suas escolhas.")
print("Se lembre, todo pedido de tempo, substituição e qualquer outro acontecimento influenciam no jogo!!!")
explicacao = input("Deseja relembrar as regras do jogo? (S/N): ")
if explicacao.upper() == "S":
    print(
        " O jogo é dividido em 2 times, onde cada um tem 6 jogadores em quadra e mais o líbero. O seu time pontua quando ocorre quando " \
        "a bola toca no chão da quadra adversária ou uma falta acontece.Falta ocorrem quando: \
             -A bola tocar no time adversário e depois bater no lado de fora da quadra;" \
             "-O time adversário tocar na rede durante um ponto;" \ 
             "-O time adversário tocar na bola mais de 3 vezes;" \
             "-Durante o saque se o jogador adversário pisar na quadra"
             
             
              
        "Lembrando que, o técnico designa 7 jogadores para cada uma das respetivas posições:" \
        " -1->Levantador: responsável por levantar a bola para os atacantes;" \
        " -1->Oposto: responsável por atacar a bola principalment;" \
        " -2->Ponteiro: reponsável por atacar e o passe;" \
        " -2->Central: reponsável por bloquear e atacar;" \
        " -1->Líbero: responsável pelo passe e defender a bola[não podendo atacar];" \
        )
print("A partir das funções dos jogadores, o técnico pode escolher a rotação do time, fazer substituições e pedir tempo. Um set só acaba" \
      "quando um time atinge 25 pontos e a diferença entre os pontos é menor do que dois," \
      "é melhor de 3 sets, isto é, é necessário ganhar 2 sets para vencer a partida. Caso aja um empate de 1 set para cada time, acontecerá um terceiro até 15 pontos."
      )

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
      "Esperamos que após avaliem nosso jogo e deem sugestões de melhorias."\
        "CRIADORES: \n -Isabelle Perin \n -Martin Jr \n -Murilo Motta \n -Thomas Ávila")
