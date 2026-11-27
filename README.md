# Trabalho_avaliativo

## SIMULADOR DE TECNICO DE VOLEIBOL (Jogo simulando uma partida de volei, onde voce e o tecnico)

```mermaid 
 classDiagram
direction TB
    class Posicao {
        <<enumeration>>
        LEVANTADOR = 1
        OPOSTO = 2
        PONTEIRO = 3
        CENTRAL = 4
        LIBERO = 5
    }

    class AreaAtaque {
        <<enumeration>>
        ENTRADA = 1
        MEIO = 2
        SAIDA = 3
        FUNDO = 4
    }

    class Jogador {
        +int FATOR_CANSACO
        +int MAXIMO_ATRIBUTOS
        +int SOMA_ALPHA_BETA
        +int TAMANHO_ATRIBUTOS
        +str nome
        +int camisa
        +Posicao posicao
        +float ataque
        +float passe
        +float levantamento
        +float saque
        +float bloqueio
        +float cansaco
        +__init__(nome: str, camisa: int, posicao: Posicao, ataque: float, passe: float, levantamento: float, saque: float, bloqueio: float): void
        -_medir_qualidade(alpha: float): float
        +sacar() float
        +receber(saque_oponente: float) float
        +levantar(passe_aliado: float) float 
        +atacar(levantamento_aliado: float) float
        +bloquear(ataque_oponente: float) float
        +defender(ataque_oponente: float, bloqueio_aliado: float) float
        +cansar(valor: int) void
        +descansar(valor: int) void

    }


    class Tecnico {
        +int TEMPOS
        +int SUBSTITUICOES
        +__init__(nome: str) void
        +str nome
        +int tempos_restantes
        +int substituicoes_restantes
        +bool quer_substituir
        +bool quer_tempo
        +pedir_substituicao() void
        +pedir_tempo() void
    }


    class Time {
        +int MAXIMO_JOGADORES
        +int MINIMO_JOGADORES
        +__init__(nome: str, jogadores: list~Jogador~, tecnico: Tecnico) void
        +str nome
        +list~Jogador~ jogadores
        +list~Jogador~ em_quadra
        +Jogador setimo
        +list~Jogador~ reservas
        +Tecnico tecnico
        +list~Posicao~ posicionamento_base
        +rodar(): void
        +entra_libero() void
        +entra_central() void
        +substituir(jogador_entrando: Jogador, jogador_saindo: Jogador) void
        +escolher_sacador() Jogador
        +escolher_receptor() Jogador
        +escolher_levantador(passador: Jogador) Jogador
        +escolher_atacante(levantador: Jogador) tuple~Jogador, AreaAtaque~
        +escolher_bloqueadores(area_ataque: AreaAtaque) list~Jogador~
        +escolher_defensor(bloqueadores: list~Jogador~) Jogador

    }

    class Placar {
        +int PONTOS_SET
        +int PONTOS_TIE_BREAK
        +int SETS_PARA_VENCER
        +int VANTAGEM_PARA_VENCER
        +list~Time~ times
        +dict~Time, int~ pontos
        +dict~Time, int~ sets
        +__init__(times: list~Time~) void
        +aumentar_pontos(time: Time) void
        +aumentar_sets(time: Time) void
        +zerar_pontos() void
        +set_em_andamento() bool
        +partida_em_andamento() bool
    }

    class Interface{
        +int LARGURA_INTERFACE
        +int PAUSA
        +float PAUSA_PONTO
        +dict~str, list~ frases
        +list~str~ bloqueios
        +list~int~ limites
        +str formato_time
        +str formato_placar
        +__init__() void
        +nivel_qualidade(qualidade: float) int
        +narrar(acao: str, jogador: Jogador, qualidade: float, errou: bool) void
        +narrar_bloqueio(bloqueadores: list~Jogador~, qualidade: float) void
        +mostrar_placar(placar: Placar, time_sacador: Time) void
        +mostrar_ponto(time: Time) void
        +mostrar_fim_set(placar: Placar, vencedor: Time) void
        +mostrar_fim_partida(placar: Placar) void
        +linha_tabela(jogador: Jogador) str
        +mostrar_time(time: Time) void
        +mostrar_tempo(time: Time) void
        +mostrar_substituicao(time: Time, entrando: Jogador, saindo: Jogador) void
        +perguntar_numero(pergunta: str, jogadores: list~Jogador~) Optional~Jogador~
        +perguntar_substituicao(time: Time) tuple~Optional~Jogador~, Optional~Jogador~~
        +mostrar_comandos(tecnico: Tecnico, placar: Placar) void
        +ler_teclas(): list~str~
    }

    class Partida {
        +int CANSACO_PULO
        +int CONSTANTE_CANSACO
        +int CONSTANTE_DESCANSO
        +int DESCANSO_TEMPO
        +int LIMIAR_ERRO
        +Placar placar
        +Interface interface
        +list~Time~ times
        +__init__(placar: Placar, interface: Interface) void
        +Time time_sacador
        +Time primeiro_sacador 
        +Time time_atacante 
        +Time time_defensor 
        +dict~str, list~ comandos
        +tempo(): void
        +conferir_teclas() void
        +atender_pedidos() void
        +atualizar_cansaco() void
        +errou_jogada(acao: str, jogador: Jogador, qualidade: float) bool
        +jogar_moeda() int
        +organizar_time_atacante() void
        +aconteceu_ponto(time_pontuou: Time) void
        +disputar_rally(qualidade_saque: float) void
        +disputar_ponto() void
        +disputar_partida() void
    }

    Partida "1" --> "1" Placar : atualiza
    Partida "1" --> "1" Interface : exibe pela
    Partida "1" --> "2" Time : times
    Placar "1" --> "2" Time : times
    Time "1" o-- "7..12" Jogador : jogadores
    Time "1" --> "1" Tecnico : tecnico
    Jogador "1" --> "1" Posicao : posicao
    Time ..> Posicao
    Time ..> AreaAtaque
    Interface ..> Jogador
    Interface ..> Time
    Interface ..> Placar
    Interface ..> Tecnico
    Interface ..> Posicao

    class Posicao:::roxoClaro
    class AreaAtaque:::cinzaClaro
    class Jogador:::amareloClaro
    class Tecnico:::vermelhoClaro
    class Time:::azulClaro
    class Placar:::verdeClaro
    class Partida:::rosaClaro
    class Interface:::laranjaClaro

    classDef rosaClaro fill:#fce7f3,stroke:#f472b6,stroke-width:2px,color:#831843
    classDef azulClaro fill:#e0f2fe,stroke:#38bdf8,stroke-width:2px,color:#0c4a6e
    classDef verdeClaro fill:#dcfce7,stroke:#4ade80,stroke-width:2px,color:#14532d
    classDef amareloClaro fill:#fef9c3,stroke:#facc15,stroke-width:2px,color:#713f12
    classDef roxoClaro fill:#f3e8ff,stroke:#c084fc,stroke-width:2px,color:#1e1b4b
    classDef cinzaClaro fill:#f3f4f6,stroke:#9ca3af,stroke-width:2px,color:#1f2937
    classDef vermelhoClaro fill:#fee2e2,stroke:#f87171,stroke-width:2px,color:#7f1d1d
    classDef laranjaClaro fill:#ffedd5,stroke:#fb923c,stroke-width:2px,color:#7c2d12
```

## Colaboradores


- [Martin](https://github.com/MartinSjr01)
- [Thomas](https://github.com/avilathomas)
- [Isabelle](https://github.com/bellemichielin)
- [Murilo](https://github.com/muriloeichholz)
