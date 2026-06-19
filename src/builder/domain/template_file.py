from dataclasses import dataclass


@dataclass
class TemplateFile:
    path: str
    content: str
