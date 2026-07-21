from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location("runtime_config", Path(__file__).with_name("runtime_config.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_find_python_dll_returns_none_when_not_found(monkeypatch):
    monkeypatch.setattr(module, "Path", lambda *args, **kwargs: Path(*args, **kwargs))
    assert module.find_python_dll() is None
