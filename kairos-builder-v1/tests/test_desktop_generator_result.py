from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_desktop_generator_result_paths_exist(tmp_path: Path):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    assert result.project_path.exists()
    assert result.project_path.is_dir()

    assert result.generated_count == 13
    assert all(path.exists() for path in result.generated_files)
    assert all(path.is_file() for path in result.generated_files)


def test_desktop_generator_result_grouped_files_exist(tmp_path: Path):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    grouped_files = (
        result.generated_pages
        + result.generated_widgets
        + result.generated_viewmodels
        + result.generated_services
        + result.generated_adapters
    )

    assert len(grouped_files) == 7
    assert all(path.exists() for path in grouped_files)
    assert all(path.is_file() for path in grouped_files)
