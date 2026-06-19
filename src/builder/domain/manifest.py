from dataclasses import dataclass


@dataclass(frozen=True)
class Manifest:
    schema: str
    builder_minimum_version: str
    project_name: str
    project_version: str
    language: str
    architecture: str
