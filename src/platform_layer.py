"""
Windows platform layer for NekoChu.

Handles:
- Transparent window via colorkey (WS_EX_LAYERED)
- Always-on-top (HWND_TOPMOST)
- Click-through on transparent pixels (automatic with WS_EX_LAYERED + colorkey)
- Hidden from taskbar and Alt+Tab (WS_EX_TOOLWINDOW)
- No focus stealing (WS_EX_NOACTIVATE)
- Real screen dimensions + taskbar height detection
- High-DPI awareness

Only uses ctypes — no pywin32 required.
"""

import ctypes
import ctypes.wintypes
import sys
from typing import Tuple

# ── Guardia de plataforma ────────────────────────────────────────────


def check_platform() -> None:
    """Lanza un error claro si no se ejecuta en Windows."""
    if sys.platform != "win32":
        raise RuntimeError(
            f"platform_layer.py requiere Windows. "
            f"Plataforma detectada: {sys.platform!r}"
        )


# ── Constantes de la Windows API ─────────────────────────────────────

GWL_EXSTYLE = -20

# Extended window styles
WS_EX_LAYERED = 0x00080000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000

# SetWindowPos flags
HWND_TOPMOST = ctypes.wintypes.HWND(-1)
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040

# SetLayeredWindowAttributes mode
LWA_COLORKEY = 0x00000001

# GetSystemMetrics índices
SM_CXSCREEN = 0
SM_CYSCREEN = 1

# DPI awareness
PROCESS_PER_MONITOR_DPI_AWARE = 2

# SystemParametersInfo
SPI_GETWORKAREA = 0x0030


# ── Declaración de tipos para ctypes ─────────────────────────────────

_user32 = ctypes.windll.user32
_shcore = ctypes.windll.shcore

_user32.GetWindowLongW.restype = ctypes.c_long
_user32.GetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]

_user32.SetWindowLongW.restype = ctypes.c_long
_user32.SetWindowLongW.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.c_long]

_user32.SetLayeredWindowAttributes.restype = ctypes.wintypes.BOOL
_user32.SetLayeredWindowAttributes.argtypes = [
    ctypes.wintypes.HWND,
    ctypes.wintypes.COLORREF,
    ctypes.wintypes.BYTE,
    ctypes.wintypes.DWORD,
]

_user32.SetWindowPos.restype = ctypes.wintypes.BOOL
_user32.SetWindowPos.argtypes = [
    ctypes.wintypes.HWND,
    ctypes.wintypes.HWND,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.wintypes.UINT,
]

_user32.SystemParametersInfoW.restype = ctypes.wintypes.BOOL
_user32.SystemParametersInfoW.argtypes = [
    ctypes.wintypes.UINT,
    ctypes.wintypes.UINT,
    ctypes.c_void_p,
    ctypes.wintypes.UINT,
]


# ── RECT auxiliar para SystemParametersInfo ───────────────────────────


class _RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


# ── API pública ───────────────────────────────────────────────────────


def enable_dpi_awareness() -> None:
    """Activa el modo Per-Monitor DPI Aware."""
    try:
        _shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    except OSError:
        try:
            _user32.SetProcessDPIAware()
        except OSError:
            pass


def get_screen_size() -> Tuple[int, int]:
    """Devuelve (ancho, alto) de la pantalla primaria en píxeles reales."""
    w = _user32.GetSystemMetrics(SM_CXSCREEN)
    h = _user32.GetSystemMetrics(SM_CYSCREEN)
    return w, h


def get_taskbar_height() -> int:
    """Devuelve el alto de la barra de tareas en píxeles."""
    rect = _RECT()
    _user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    _, screen_h = get_screen_size()
    return screen_h - rect.bottom


def _rgb_to_colorref(r: int, g: int, b: int) -> int:
    """Convierte un color RGB de Python a COLORREF de Windows."""
    return r | (g << 8) | (b << 16)


def setup_transparent_window(
    hwnd: int,
    colorkey: Tuple[int, int, int],
) -> None:
    """
    Configura la ventana de pygame como overlay de escritorio transparente.
    """
    ex_style = _user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    new_ex_style = ex_style | WS_EX_LAYERED | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
    _user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_ex_style)

    colorref = _rgb_to_colorref(*colorkey)
    ok = _user32.SetLayeredWindowAttributes(hwnd, colorref, 0, LWA_COLORKEY)
    if not ok:
        raise RuntimeError("SetLayeredWindowAttributes falló.")

    _user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0,
        0,
        0,
        0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW,
    )


def refresh_topmost(hwnd: int) -> None:
    """Re-aplica el estado always-on-top."""
    _user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0,
        0,
        0,
        0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
    )
