from dataclasses import dataclass


@dataclass
class RepositoryInfo:
    name: str
    path: str
    language: str
    architecture: str
    manifest_found: bool
    git_found: bool
    branch: str
    source_files: int
    test_files: int
    directories: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "language": self.language,
            "architecture": self.architecture,
            "manifest_found": self.manifest_found,
            "git_found": self.git_found,
            "branch": self.branch,
            "source_files": self.source_files,
            "test_files": self.test_files,
            "directories": self.directories,
        }
