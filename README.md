# Trabalho_avaliativo

## SIMULADOR DE TECNICO DE VOLEIBOL(Jogo simulado de volei, onde voce e o tecnico)

```mermaid 
 classDiagram
direction TB
    class Times {
        +Jogadores jogadores
        +String Nome
        +String Nome2
    }

    class Placar {
        +int pontuacao1
        +int pontuacao2
        +int rotacao
        +int tempo
    }

    class Jogadores {
        +String oposto
        +String levantador
        +String libero
        +String ponteiro1
        +String ponteiro2
        +String central1
        +String central2
        +String Reservas
    }

    class Tecnico {
        +int pedirtempo
        +int pedirsubst
    }

    class Jogo {
        +Times times
        +Placar placar
        +Tecnico tecnico
    }

    Jogo "1" --> "*" Times : Primeiro
    Jogo "2" --> "*" Placar : segundo
    Times "2.1" --> "*" Jogadores : Segundo
    Jogo "3" --> "*" Tecnico : terceiro
    Jogadores "2.1.0" --> "*" Reservas

    class Times:::azulClaro
    class Placar:::verdeClaro
    class Jogadores:::amareloClaro
    class Jogo:::rosaClaro

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
