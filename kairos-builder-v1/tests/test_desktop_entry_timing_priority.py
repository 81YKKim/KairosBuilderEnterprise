from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_detail_contains_entry_timing_priority_styles(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    detail_source = (
        desktop_root
        / "widgets"
        / "recommendation_detail.py"
    ).read_text(encoding="utf-8")

    theme_source = (
        desktop_root
        / "theme.py"
    ).read_text(encoding="utf-8")

    assert "ENTRY_TIMING_STYLE_NAMES" in detail_source
    assert '"BUY NOW": "entryTimingBuyNow"' in detail_source
    assert '"SPLIT BUY": "entryTimingSplitBuy"' in detail_source
    assert '"WAIT PULLBACK": "entryTimingWaitPullback"' in detail_source
    assert '"DO NOT CHASE": "entryTimingDoNotChase"' in detail_source
    assert "_apply_entry_timing_style" in detail_source

    assert "QLabel#entryTimingBuyNow" in theme_source
    assert "QLabel#entryTimingSplitBuy" in theme_source
    assert "QLabel#entryTimingWaitPullback" in theme_source
    assert "QLabel#entryTimingDoNotChase" in theme_source
    assert "#EF4444" in theme_source


def test_generated_adapter_contains_do_not_chase_state(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    adapter_source = (
        desktop_root
        / "adapters"
        / "replay_adapter.py"
    ).read_text(encoding="utf-8")

    assert "KAIROS-D" in adapter_source
    assert "DO NOT CHASE" in adapter_source
    assert "entry timing threshold" in adapter_source