from pathlib import Path

from builder.generator.desktop_generator import DesktopGenerator


def test_generated_desktop_python_files_do_not_use_utf8_bom(
    tmp_path: Path,
):
    result = DesktopGenerator().generate(
        "KairosDesktop",
        str(tmp_path),
    )

    python_files = tuple(
        result.project_path.rglob("*.py")
    )

    assert python_files

    bom_files = tuple(
        path.relative_to(result.project_path)
        for path in python_files
        if path.read_bytes().startswith(b"\xef\xbb\xbf")
    )

    assert bom_files == ()


def test_desktop_templates_do_not_use_utf8_bom():
    template_root = Path("templates") / "desktop"

    template_files = tuple(
        template_root.rglob("*.tpl")
    )

    assert template_files

    bom_templates = tuple(
        path
        for path in template_files
        if path.read_bytes().startswith(b"\xef\xbb\xbf")
    )

    assert bom_templates == ()
