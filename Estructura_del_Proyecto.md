pokemon_roguelite/
├── assets/                # Archivos gráficos y de sonido
│   ├── sprites/           # Sprites de personajes, Pokémon, etc.
│   ├── backgrounds/       # Fondos de los niveles y batallas
│   ├── audio/             # Efectos de sonido y música
│   └── ui/                # Elementos de la interfaz de usuario
├── config/                # Configuración del juego
│   ├── settings.py        # Configuración general (opciones de juego)
│   └── levels_config.py   # Configuración de niveles, arcos, etc.
├── data/                  # Datos persistentes del juego
│   ├── save_files/        # Archivos de guardado
│   └── database/          # Base de datos para objetos, Pokémon, habilidades
│       └── game.db        # Base de datos SQLite
├── docs/                  # Documentación
│   └── project_plan.docx  # Documento de planificación y fases
├── src/                   # Código fuente
│   ├── core/              # Componentes principales del juego
│   │   ├── combat.py      # Sistema de combate
│   │   ├── player.py      # Clase del jugador
│   │   ├── pokemon.py     # Lógica de Pokémon
│   │   └── event.py       # Eventos aleatorios y narrativa
│   ├── ui/                # Interfaz gráfica del usuario
│   │   ├── main_menu.py   # Menú principal
│   │   └── battle_ui.py   # Interfaz para las batallas
│   ├── levels/            # Generación de niveles
│   │   ├── level.py       # Clases y lógica de niveles
│   │   └── level_generator.py # Generador de niveles aleatorios
│   └── main.py            # Punto de entrada del juego
├── tests/                 # Pruebas unitarias
│   ├── test_combat.py     # Pruebas del sistema de combate
│   ├── test_events.py     # Pruebas de los eventos aleatorios
│   └── test_player.py     # Pruebas de la lógica del jugador
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Descripción del proyecto
