import difflib

class DiffGenerator:
    def create_diff(self, old: str, new: str) -> str:
        diff = difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            lineterm=""
        )
        return "\n".join(diff)