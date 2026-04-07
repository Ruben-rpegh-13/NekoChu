# NekoChu - Pikachu Desktop Pet

Mascota de escritorio animada de Pikachu que sigue el cursor.

## Uso

1. Haz doble clic en `run.bat`
2. ¡Listo! Pikachu persigue tu cursor
3. Presiona **ESC** para cerrar

## Requisitos

- Windows 7/8/10/11
- Python 3.8+ (instalado automáticamente si falta)

## Controles

| Acción | Descripción |
|--------|-------------|
| Mover mouse | Pikachu te sigue |
| Click + arrastrar | Arrastra a Pikachu |
| 10s inactivo | Pikachu se duerme |
| Cualquier tecla/movimiento | Despierta a Pikachu |
| ESC | Cerrar aplicación |

## Estructura

```
NekoChu/
├── run.bat           # Ejecutable (doble clic)
├── main.py           # Punto de entrada
├── config.py         # Configuración
├── sprites/          # Sprites de Pikachu
└── Src/
    ├── entity.py     # Clase Entity
    ├── movement.py   # Lógica de movimiento
    └── animation.py  # Carga de sprites
```
