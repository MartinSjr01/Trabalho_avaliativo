---
# Trabalho_avaliativo
----
Projeto-POO
---
```mermaid
classDiagram
    %% Configuração do Tema
    %% config: { "theme": "forest" }

    %% Definição de Estilos em Cores Claras (Pastel)
    classDef rosaClaro fill:#fce7f3,stroke:#f472b6,stroke-width:2px,color:#831843;
    classDef azulClaro fill:#e0f2fe,stroke:#38bdf8,stroke-width:2px,color:#0c4a6e;
    classDef verdeClaro fill:#dcfce7,stroke:#4ade80,stroke-width:2px,color:#14532d;
    classDef amareloClaro fill:#fef9c3,stroke:#facc15,stroke-width:2px,color:#713f12;
    classDef roxoClaro fill:#f3e8ff,stroke:#c084fc,stroke-width:2px,color:#1e1b4b;

    %% Aplicação das Classes e seus Estilos
    class Jogo:::rosaClaro {
        +Times times
        +Placar placar
    }

    class Times:::azulClaro {
        +Jogadores jogadores
        +String tecnico
    }

    class Placar:::verdeClaro {
        +int pontuacao
        +int rotacao
    }

    class Jogadores:::amareloClaro {
        +String oposto
        +String levantador
        +String libero
        +String ponteiro1
        +String ponteiro2
        +String central1
        +String central2
    }

    %% Relacionamentos de Composição/Associação entre Classes
    Jogo "1" -- "2" Times : possui
    Jogo "1" -- "1" Placar : possui
    Times "1" -- "1" Jogadores : possui

TIME JOAO

[Martin](https://github.com/MartinSjr01)
[Thomás](https://github.com/avilathoma)
[Isabelle](https://github.com/bellemichielin)






TIME JOAO

[Martin](https://github.com/MartinSjr01)
[Thomás](https://github.com/avilathoma)
[Isabelle](https://github.com/bellemichielin)
