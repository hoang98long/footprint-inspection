"""ASGI compatibility entry point for ``uvicorn app.main:app``.

Application composition remains in :mod:`app.application`.
"""

from app.application import create_application

app = create_application()
