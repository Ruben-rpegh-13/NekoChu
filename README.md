# NekoChu ⚡

**NekoChu** es una mascota de escritorio animada inspirada en el clásico *Oneko*. Es **Pikachu** que persigue el cursor del ratón por tu pantalla.

---

## 🎮 Características

- Pikachu animado que persigue el cursor del ratón (movimiento 2D fluido)
- Animaciones: walk, idle, drag, sleep, annoyed, rage, jump, fall, dust
- **Sprites animados** de PokeAPI (Gen 5) y WikiDex
- Sistema de **enfado progresivo**: 5 clics = mensajes de advertencia
- **Animación RAGE**: Tras agotar advertencias, Pikachu libera un rayo ⚡
- Sistema de sueño por inactividad (10 segundos)
- Sistema de arrastre con mouse (drag & drop)
- **Física**: Gravedad solo tras soltar en el aire → efecto de polvo al aterrizar
- Burbujas de texto con mensajes
- Efecto de rayos (lightning bolts) durante rage
- Estructura modular

---

## 📁 Estructura del proyecto

```
NekoChu/
├── main.py              # Punto de entrada
├── config.py            # Configuración centralizada
├── sprites/
│   ├── pokeapi/       # Sprites animados de PokeAPI
│   │   ├── pikachu_walk.gif    # Gen 5 B&W animado
│   │   └── pikachu_crystal.gif  # Gen 2 Crystal animado
│   └── wikidex/       # Sprites de WikiDex
│       ├── sleep.png    # Dormido (PLB)
│       └── angry.png    # Enfadado (PLB)
└── src/             # Módulos
    ├── entity.py      # Clase Entity
    ├── movement.py   # Lógica de movimiento
    ├── animation.py  # Carga de sprites/GIFs
    ├── sleep.py    # Sistema de sueño
    ├── interaction.py  # Tracking de clicks
    └── effects.py  # Burbujas y rayos
```

---

## ⚙️ Requisitos

```bash
pip install pygame Pillow
```

---

## 🚀 Uso

```bash
python main.py
```

---

## 🎮 Controles

| Acción | Efecto |
|--------|--------|
| Mover mouse | Pikachu persigue el cursor |
| Click en Pikachu (5 veces rápido) | Mensajes: "¡Pii!" → "¡Pika!" → "¡PIKA-CHU!" |
| 5+ clicks | Rabia total → Rayos ⚡ |
| Drag & Drop | Arrastrar a Pikachu |
| Soltar en aire | Caída + polvo al aterrizar |
| Tecla S | Forzar estado dormir |
| Tecla A | Forzar estado molesto |
| Tecla R | Forzar estado rabia |
| 10s inactivo | Auto-dormir |
| Movimiento | Despierta a Pikachu |
| ESC | Cerrar programa |

### Sistema de Enfado

1. **5 clics rápidos** → Primer mensaje
2. **5 más** → Siguiente mensaje...
3. **5+ total** → ¡RAGE! con rayos

---

## 🛠️ Configuración

Edita `config.py`:

```python
SPEED = 6                    # Velocidad de movimiento
STOP_DISTANCE = 10           # Distancia para detenerse
SLEEP_TIMEOUT = 10.0       # Segundos hasta dormir
ANNOYANCE_DURATION = 3.0     # Duración del estado annoyed
RAGE_DURATION = 4.0          # Duración de rage
GRAVITY = 1200              # Gravedad tras drop
SPRITE_SIZE = 64             # Tamaño del sprite
```

---

## 📝 Sprites

Los sprites se cargan automáticamente de:
- **walk**: PokeAPI Gen 5 B&W animated
- **idle**: PokeAPI Gen 2 Crystal animated
- **sleep**: WikiDex (Pikachu dormido)
- **annoyed**: WikiDex (Pikachu enfadado)
- **drag/idle direction**: Versiones volteadas automáticamente

---

## 📝 Licencia

Libre para uso personal y educativo.