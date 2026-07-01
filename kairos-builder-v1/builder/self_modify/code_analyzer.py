import ast

class CodeAnalyzer:
    def analyze(self, source_code: str) -> dict:
        tree = ast.parse(source_code)

        functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

        return {
            "functions": functions,
            "classes": classes,
            "complexity": len(functions) + len(classes)
        }