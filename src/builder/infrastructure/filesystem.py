from pathlib import Path


class Filesystem:
    def exists(self, path: str) -> bool:
        return Path(path).exists()

    def project_name(self, path: str) -> str:
        return Path(path).name

    def git_found(self, path: str) -> bool:
        return (Path(path) / ".git").exists()

    def manifest_found(self, path: str, manifest_name: str = "builder.manifest.json") -> bool:
        return (Path(path) / manifest_name).exists()

    def count_directories(self, path: str) -> int:
        root = Path(path)
        if not root.exists():
            return 0

        return sum(1 for item in root.rglob("*") if item.is_dir())

    def count_source_files(self, path: str) -> int:
        root = Path(path)
        if not root.exists():
            return 0

        return sum(
            1
            for item in root.rglob("*.py")
            if item.is_file() and "tests" not in item.parts
        )

    def count_test_files(self, path: str) -> int:
        root = Path(path)
        if not root.exists():
            return 0

        return sum(
            1
            for item in root.rglob("test_*.py")
            if item.is_file()
        )
