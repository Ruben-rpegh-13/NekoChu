# NekoChu ⚡

**NekoChu** es una mascota de escritorio animada inspirada en el clásico *Oneko*. En lugar de un gato, es **Pikachu** que persigue el cursor del ratón por tu pantalla.

Soporta **Windows** (Pygame/SDL) y **Linux** (Pygame/SDL o GTK con click-through).

---

## 🎨 Características

- Pikachu animado que persigue el cursor del ratón
- Animaciones por frames: caminar, idle, dormir, arrastre y estado "molesto"
- Sistema de **enfado progresivo**: 8 mensajes de advertencia antes del colapso
- **Animación RAGE**: Después de agotar todas las advertencias, Pikachu libera un rayo con efecto visual
- Sistema de sueño por inactividad (10 segundos)
- Sistema de arrastre con mouse
- Burbujas de texto con mensajes
- Efecto de rayos (lightning bolts) durante el estado rage
- Click-through transparent window (GTK/Linux)
- Estructura modular y fácil de extender

---

## 📁 Estructura del proyecto

```
NekoChu-main/
├── main.py              # Punto de entrada Pygame (Windows/Linux)
├── main_gtk.py          # Punto de entrada GTK (Linux con click-through)
├── config.py            # Configuración centralizada
├── sprites/
│   └── pikachu64.png    # Sprite sheet 256x256 (4 filas x 4 columnas)
└── src/                 # Módulos (versión Pygame)
    ├── entity.py         # Clase Entity
    ├── movement.py      # Lógica de movimiento
    ├── animation.py     # Carga de sprite sheets
    ├── sleep.py         # Sistema de sueño
    ├── interaction.py   # Tracking de clicks
    └── effects.py       # Burbujas de texto y efectos
```

### Formato del Sprite Sheet

El archivo `sprites/pikachu64.png` debe tener **256x256 píxeles** con frames de **64x64**:

| Fila | Animación | Dirección |
|------|-----------|-----------|
| 0    | Caminar   | Derecha   |
| 1    | Caminar   | Izquierda |
| 2    | Idle      | Derecha   |
| 3    | Idle      | Izquierda |

---

## ⚙️ Requisitos

### Versión Pygame (main.py) - Windows/Linux

```bash
pip install pygame
```

### Versión GTK (main_gtk.py) - Linux

```bash
# Dependencias del sistema
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgdk-pixbuf2.0-dev libcairo2-dev

# Dependencias de Python
pip install pygobject python-xlib
```

---

## 🚀 Uso

### Windows o Linux (Pygame)
```bash
python main.py
```

### Linux con Click-through (GTK)
```bash
python main_gtk.py
```

> **Nota**: La versión GTK crea una ventana transparente donde solo el sprite de Pikachu captura clics, permitiendo interactuar con otras ventanas debajo.

---

## 🎮 Controles

| Acción | Efecto |
|--------|--------|
| Mover mouse | Pikachu persigue el cursor |
| Clic en Pikachu (5 veces rápido) | Pikachu muestra mensaje de advertencia |
| 8 advertencias agotadas | **¡PIKACHU SE ENFURECE!** → Animación RAGE + Rayo |
| Clic fuera y arrastrar | Arrastra a Pikachu |
| Inactividad 10 segundos | Pikachu se duerme |
| Cualquier tecla | Despierta a Pikachu (o calma si está enojado/rage) |
| ESC | Salir del programa |

### Sistema de Enfado Progresivo

1. **5 clics rápidos** → Muestra primer mensaje de advertencia
2. **5 clics más** → Siguiente mensaje...
3. **Tras 8 advertencias** → ¡COLAPSO! Pikachu libera **Thunder Shock**
4. **15 segundos de cooldown** antes de poder activar rage de nuevo

---

## 🛠️ Configuración

Edita `config.py` para personalizar:

```python
SPEED = 2.5                    # Velocidad de movimiento
STOP_DISTANCE = 10             # Distancia para detenerse
SLEEP_TIMEOUT = 10.0           # Segundos hasta dormir
ANNOYANCE_CLICKS = 5           # Clics para cada advertencia
ANNOYANCE_DURATION = 3.0       # Duración del estado enojado
ANNOYANCE_MESSAGE_DURATION = 0.8  # Duración de cada mensaje
RAGE_DURATION = 4.0            # Duración de la animación RAGE
RAGE_COOLDOWN = 15.0           # Cooldown entre rages
FRAME_WIDTH = 64               # Ancho del frame
FRAME_HEIGHT = 64             # Alto del frame
```

---

## 📝 Licencia

Libre para uso personal y educativo.
