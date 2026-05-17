import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON_ROOTS = (
    ROOT / "src" / "earnings_call_risk_map",
    ROOT / "scripts",
)


class ImportHygieneTests(unittest.TestCase):
    def test_project_imports_are_top_level(self):
        for root in PYTHON_ROOTS:
            for path in sorted(root.rglob("*.py")):
                with self.subTest(path=path.relative_to(ROOT).as_posix()):
                    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                    nested_imports = [
                        node.lineno
                        for node in ast.walk(tree)
                        if isinstance(node, (ast.Import, ast.ImportFrom)) and not _is_top_level_import(tree, node)
                    ]
                    self.assertEqual([], nested_imports)


def _is_top_level_import(tree, target):
    return any(target is node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom)))
