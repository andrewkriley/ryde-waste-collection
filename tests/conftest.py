"""Load the integration package without importing Home Assistant."""
from __future__ import annotations

from pathlib import Path
import sys
import types

PKG_DIR = (
    Path(__file__).resolve().parents[1]
    / "custom_components"
    / "ryde_waste_collection"
)
if "ryde_waste_collection" not in sys.modules:
    pkg = types.ModuleType("ryde_waste_collection")
    pkg.__path__ = [str(PKG_DIR)]
    sys.modules["ryde_waste_collection"] = pkg
