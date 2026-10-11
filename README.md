```mermaid
classDiagram
    %% Configuração de Estilos em Cores Claras (Pastel)
    classDef rosaClaro fill:#fce7f3,stroke:#f472b6,stroke-width:2px,color:#831843;
    classDef azulClaro fill:#e0f2fe,stroke:#38bdf8,stroke-width:2px,color:#0c4a6e;
    classDef verdeClaro fill:#dcfce7,stroke:#4ade80,stroke-width:2px,color:#14532d;
    classDef amareloClaro fill:#fef9c3,stroke:#facc15,stroke-width:2px,color:#713f12;

    %% Definição das Classes
    class Jogo {
        +Times times
        +Placar placar
        +iniciarPartida()
        +atualizarPlacar()
    }

    class Times {
        +String nome
        +String tecnico
        +List~Jogador~ jogadores
        +adicionarJogador()
    }

    class Jogador {
        +String nome
        +int numero
        +String posicao
        +sacar()
        +atacar()
    }

    class Placar {
        +int pontosEquipe1
        +int pontosEquipe2
        +int rotacao
        +incrementarPonto()
    }

    %% Aplicação dos Estilos
    class Jogo rosaClaro
    class Times azulClaro
    class Jogador amareloClaro
    class Placar verdeClaro

    %% Relacionamentos de POO (Associação, Composição e Multiplicidade)
    Jogo "1" -- "2" Times : possui >
    Jogo "1" -- "1" Placar : gerencia >
    Times "1" *-- "* " Jogador : comanda (possui) >
