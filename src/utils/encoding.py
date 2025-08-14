"""
Encoding utilities for cross-platform compatibility.
"""

import sys


def configure_encoding() -> None:
    """
    Configura la codificación UTF-8 para stdout y stderr.
    
    Esta función es especialmente útil en Windows para asegurar
    que la salida se muestre correctamente con caracteres Unicode.
    """
    try:
        # Reconfigurar stdout y stderr para usar UTF-8
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        # Si falla la reconfiguración, continuar sin cambios
        pass 