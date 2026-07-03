from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_detail_contains_ai_intelligence_fields(
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

    assert "ai_score_label" in detail_source
    assert "entry_timing_label" in detail_source
    assert "evidence_label" in detail_source
    assert '"AI Score"' in detail_source
    assert '"Entry Timing"' in detail_source
    assert '"Evidence"' in detail_source


def test_generated_replay_adapter_contains_ai_intelligence_data(
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

    assert '"ai_score"' in adapter_source
    assert '"entry_timing"' in adapter_source
    assert '"evidence"' in adapter_source
    assert "BUY NOW" in adapter_source
    assert "SPLIT BUY" in adapter_source
    assert "WAIT PULLBACK" in adapter_source


def test_generated_theme_contains_detail_intelligence_style(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    desktop_root = result.project_path / "src" / "desktop"

    theme_source = (
        desktop_root
        / "theme.py"
    ).read_text(encoding="utf-8")

    assert "recommendationDetail" in theme_source
    assert "detailTitle" in theme_source
    assert "detailSummaryFrame" in theme_source
    assert "detailIntelligenceFrame" in theme_source