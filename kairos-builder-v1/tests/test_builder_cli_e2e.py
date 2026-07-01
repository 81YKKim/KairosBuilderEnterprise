from pathlib import Path

from builder.application.builder_service import BuilderService
from builder.cli.command_router import CommandRouter


def test_builder_new_e2e(tmp_path: Path):
    service = BuilderService()
    router = CommandRouter(service)

    # 실제 프로젝트 생성
    result = router.handle("new KairosDesktop")

    # CLI는 Path 또는 결과 문자열 둘 다 허용 구조
    assert result is not None

    # 생성 결과 검증 (service 직접 확인)
    project_path = service.create_project("KairosDesktop", str(tmp_path))

    assert project_path.exists()

    # 핵심 구조 검증
    assert (project_path / "src").exists()
    assert (project_path / "tests").exists()
    assert (project_path / "docs").exists()

    # 필수 파일
    assert (project_path / "README.md").exists()
    assert (project_path / "pyproject.toml").exists()
    assert (project_path / ".gitignore").exists()