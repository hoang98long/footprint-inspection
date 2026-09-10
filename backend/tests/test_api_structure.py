"""Kiểm tra các thành phần API độc lập khỏi hạ tầng PostgreSQL."""

from pathlib import Path


def test_application_entrypoint_is_thin() -> None:
    content = Path("main.py").read_text(encoding="utf-8")
    assert "create_application" in content
    assert "@app." not in content


def test_uvicorn_compatibility_entrypoint_is_thin() -> None:
    content = Path("app/main.py").read_text(encoding="utf-8")
    assert "create_application" in content
    assert "@app." not in content


def test_versioned_api_modules_exist() -> None:
    router_root = Path("app/api/v1/routers")
    assert {"auth.py", "cases.py", "analysis.py", "system.py"}.issubset(
        {item.name for item in router_root.iterdir()}
    )
