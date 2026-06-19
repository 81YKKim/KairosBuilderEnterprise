import json
import subprocess
from pathlib import Path

from builder.domain.repository_info import RepositoryInfo
from builder.infrastructure.filesystem import Filesystem


class RepositoryScanner:
    def __init__(self, filesystem: Filesystem | None = None) -> None:
        self.filesystem = filesystem or Filesystem()

    def scan(self, path: str) -> RepositoryInfo:
        project_path = Path(path)

        language = self._detect_language(project_path)
        architecture = self._detect_architecture(project_path)
        branch = self._detect_branch(project_path)

        return RepositoryInfo(
            name=self.filesystem.project_name(path),
            path=str(project_path),
            language=language,
            architecture=architecture,
            manifest_found=self.filesystem.manifest_found(path),
            git_found=self.filesystem.git_found(path),
            branch=branch,
            source_files=self.filesystem.count_source_files(path),
            test_files=self.filesystem.count_test_files(path),
            directories=self.filesystem.count_directories(path),
        )

    def _detect_language(self, path: Path) -> str:
        if (path / "pyproject.toml").exists() or (path / "src").exists():
            return "Python"

        if any(path.rglob("*.csproj")):
            return "C#"

        if any(path.rglob("pom.xml")):
            return "Java"

        return "Unknown"

    def _detect_architecture(self, path: Path) -> str:
        manifest_path = path / "builder.manifest.json"

        if not manifest_path.exists():
            return "Unknown"

        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            return data.get("architecture", "Unknown")
        except json.JSONDecodeError:
            return "Unknown"

    def _detect_branch(self, path: Path) -> str:
        if not (path / ".git").exists():
            return "Unknown"

        try:
            result = subprocess.run(
                ["git", "-C", str(path), "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=False,
            )
            branch = result.stdout.strip()
            return branch if branch else "Unknown"
        except OSError:
            return "Unknown"
