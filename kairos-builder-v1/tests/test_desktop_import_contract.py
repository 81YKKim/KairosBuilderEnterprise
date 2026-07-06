from __future__ import annotations

import importlib
import sys
from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_modules_are_importable(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    src_root = result.project_path / "src"
    sys.path.insert(0, str(src_root))

    try:
        assert importlib.import_module("desktop") is not None
        assert importlib.import_module("desktop.app") is not None
        assert importlib.import_module("desktop.main") is not None
        assert importlib.import_module("desktop.main_window") is not None
        assert importlib.import_module("desktop.theme") is not None
        assert importlib.import_module("desktop.pages.dashboard") is not None
        assert importlib.import_module("desktop.widgets.sidebar") is not None
        assert importlib.import_module("desktop.widgets.recommendation_table") is not None
        assert importlib.import_module("desktop.widgets.recommendation_detail") is not None
        assert importlib.import_module("desktop.viewmodels.dashboard_view_model") is not None
        assert importlib.import_module("desktop.services.market_service") is not None
        assert importlib.import_module("desktop.adapters.replay_adapter") is not None
    finally:
        sys.path.remove(str(src_root))
