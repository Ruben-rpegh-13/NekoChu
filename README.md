# NekoChu 🐱⚡

**NekoChu** es una mascota de escritorio animada inspirada en el clásico *Oneko*, pero en lugar de un gato, es **Pikachu** que sigue el cursor del ratón.  

Funciona en **Windows y Linux** usando Python y Pygame.

---

## 🎨 Características

- Pikachu animado que persigue el cursor.
- Animaciones por frames: caminar e idle.
- Cambio de dirección izquierda/derecha automáticamente.
- Proyecto multiplataforma (Windows y Linux).
- Estructura modular y fácil de extender.

---

## 📁 Estructura del proyecto
├── main.py # Punto de entrada
├── config.py # Configuración del juego
├── sprites/
│ └── pikachu.png # Sprite sheet de NekoChu
└── src/
├── entity.py # Clase de la mascota
├── movement.py # Lógica de movimiento
└── animation.py # Carga y manejo de animaciones


---

## ⚙️ Requisitos

- Python 3.x
- Pygame

Instalación de Pygame:

```bash
pip install pygame
