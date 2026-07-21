import os
import sys
from pathlib import Path


def find_python_dll() -> str | None:
    """Locate a bundled python3*.dll for pythonnet on frozen Windows builds."""
    if getattr(sys, "frozen", False):
        candidates = [Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))]
        candidates.append(candidates[0] / "_internal")
        candidates.append(Path(sys.executable).resolve().parent)
    else:
        candidates = [Path(sys.executable).resolve().parent, Path(sys.prefix), Path(sys.base_prefix)]

    for base in candidates:
        if not base:
            continue
        for pattern in ("python3*.dll", "python*.dll"):
            matches = sorted(base.glob(pattern))
            if matches:
                return str(matches[0].resolve())

    return None


def configure_pythonnet_runtime() -> str | None:
    """Configure pythonnet so the Windows runtime can resolve the embedded Python DLL."""
    existing = os.environ.get("PYTHONNET_PYDLL")
    if existing:
        return existing

    dll_path = find_python_dll()
    if dll_path:
        os.environ["PYTHONNET_PYDLL"] = dll_path
        return dll_path

    return None


def configure_pythonnet_runtime_before_webview() -> None:
    configure_pythonnet_runtime()

    try:
        from pythonnet import set_runtime

        set_runtime("netfx")
    except Exception:
        pass
