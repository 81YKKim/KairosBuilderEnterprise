from dataclasses import dataclass


@dataclass
class GenerationRequest:
    target_type: str
    name: str
    output_path: str
