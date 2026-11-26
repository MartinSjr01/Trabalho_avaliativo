# Trabalho_avaliativo

## SIMULADOR DE TECNICO DE VOLEIBOL(Jogo simulado de volei, onde voce e o tecnico)

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
        +String nome
        +int camisa
        +Posicao posicao
        +float ataque
        +float passe
        +float levantamento
        +float saque
        +float bloqueio
        +float cansaco
        +__init__(nome: str, camisa: int, posicao: Posicao, ataque: float,
                passe: float, levantamento: float, saque: float, bloqueio: float): void
        +_medir_qualidade(alpha: float): float
        +sacar: (float): float
        +receber: (saqueoponente: float): float
        +levantar: (passealiado: float): float 
        +bloquear: (ataque_oponente: float): float
        +defender: (ataque_oponente: float, bloqueio_aliado: float): float
        +cansar: (valor: int): void
        +descansar: (valor: int): void

    }


    class Tecnico {
        +__init__(nome: str): void
        +string nome
        +float tempos_restantes
        +float substituicoes_restantes
        +float quer_substituir
        +float quer_tempo
        +pedir_substituicao: (): void
        +pedir_tempo: (): void
    }


    class Time {
        +__init__(nome: str, jogadores: list~Jogador~, tecnico: Tecnico): void
        +string nome
        +string jogadores
        +list~Jogador~ em_quadra
        +Jogador setimo
        +list~Jogador~ reservas
        +string tecnico
        +list~Posicao~ posicionamento_base
        +rodar: (): void
        +entra_libero: (): void
        +entra_central: (): void
        +substituir: (jogador_entrando: Jogador, jogador_saindo: Jogador): void
        +escolher_sacador: (): Jogador
        +escolher_receptor: (): Jogador
        +escolher_levantador: (passador: Jogador): Jogador
        +escolher_atacante: (levantador: Jogador): tuple~Jogador, AreaAtaque~
        +escolher_bloqueadores: (area_ataque: AreaAtaque): list~Jogador~
        +escolher_defensor: (bloqueadores: list~Jogador~): Jogador

    }

    class Placar {
        +__init__(times: list~Time~): void
        +aumentar_pontos: (time: Time): void
        +aumentar_sets: (time: Time): void
        +zerar_pontos: (): void
        +set_em_andamento: (): bool
        +partida_em_andamento: (): bool
    }

    class Partida {
        +__init__(placar: Placar, interface: Interface): void
        +float placar 
        +Interface interface 
        +float times
        +float time_sacador
        +float primeiro_sacador 
        +float time_atacante 
        +float time_defensor 
        +float organizar_time_atacante
        +      organizar_time_atacante
        +      comandos
        +tempo: (): void
        +conferir_teclas: (): void
        +atender_pedidos: (): void
        +atualizar_cansaco: (): void
        +errou_jogada: (acao: str, jogador: Jogador, qualidade: float): bool
        +jogar_moeda: (): int
        +organizar_time_atacante: (): void
        +aconteceu_ponto: (time_pontuou: Time): void
        +disputar_rally: (qualidade_saque: float): void
        +disputar_ponto: (): void
        +disputar_partida: (): void
    }

    
    Jogo "1" --> "*" Times : Primeiro
    Jogo "2" --> "*" Placar : segundo
    Times "2.1" --> "*" Jogadores : Segundo
    Jogo "3" --> "*" Tecnico : terceiro
    Jogadores "2.1.0" --> "*" Reservas

    class Posicao:::roxoClaro
    class AreaAtaque:::cinzaClaro
    class Jogador:::amareloClaro
    class Tecnico:::vermelhoClaro
    class Time:::azulClaro
    class Placar:::verdeClaro
    class Partida:::rosaClaro

    classDef rosaClaro fill:#fce7f3,stroke:#f472b6,stroke-width:2px,color:#831843
    classDef azulClaro fill:#e0f2fe,stroke:#38bdf8,stroke-width:2px,color:#0c4a6e
    classDef verdeClaro fill:#dcfce7,stroke:#4ade80,stroke-width:2px,color:#14532d
    classDef amareloClaro fill:#fef9c3,stroke:#facc15,stroke-width:2px,color:#713f12
    classDef roxoClaro fill:#f3e8ff,stroke:#c084fc,stroke-width:2px,color:#1e1b4b
```

## Colaboradores


- [Martin](https://github.com/MartinSjr01)
- [Thomas](https://github.com/avilathomas)
- [Isabelle](https://github.com/bellemichielin)
- [Murilo](https://github.com/muriloeichholz)
