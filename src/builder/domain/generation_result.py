from dataclasses import dataclass


@dataclass
class GenerationResult:
    target_type: str
    name: str
    output_path: str
    created: bool
