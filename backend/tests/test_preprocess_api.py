"""Route registration regression test without requiring a local PostgreSQL driver."""

from pathlib import Path


def test_preprocessing_endpoint_is_versioned() -> None:
    router = Path("app/api/v1/router.py").read_text(encoding="utf-8")
    endpoint = Path("app/api/v1/routers/preprocess.py").read_text(encoding="utf-8")
    assert "preprocess.router" in router
    assert '@router.post("/preprocess"' in endpoint
