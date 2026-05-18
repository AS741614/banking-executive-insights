import ast
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple

class DependencyAnalyzer:
    """
    Advanced AST-based dependency analyzer to detect circular imports.
    """
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.graph: Dict[str, Set[str]] = {}

    def _get_module_name(self, file_path: Path) -> str:
        rel_path = file_path.relative_to(self.root_dir)
        parts = list(rel_path.parts)
        if parts[-1] == "__init__.py":
            parts.pop()
        else:
            parts[-1] = parts[-1].replace(".py", "")
        return ".".join(parts)

    def build_graph(self):
        """Builds a directed graph of internal module dependencies."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    module_name = self._get_module_name(file_path)
                    self.graph[module_name] = self._extract_imports(file_path)

    def _extract_imports(self, file_path: Path) -> Set[str]:
        imports = set()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if self._is_internal(alias.name):
                            imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module and self._is_internal(node.module):
                        imports.add(node.module)
        except Exception:
            pass
        return imports

    def _is_internal(self, module_name: str) -> bool:
        # Simple heuristic: if it starts with one of our top-level packages
        top_levels = {"ai", "app", "os", "runtime", "ui", "src", "orchestration"}
        return any(module_name.startswith(f"{tl}") for tl in top_levels)

    def find_cycles(self) -> List[List[str]]:
        """Finds all cycles in the dependency graph using DFS."""
        cycles = []
        visited = set()
        stack = []

        def visit(node, path):
            if node in path:
                cycle = path[path.index(node):] + [node]
                cycles.append(cycle)
                return
            if node in visited:
                return

            visited.add(node)
            path.append(node)
            for neighbor in self.graph.get(node, []):
                visit(neighbor, path)
            path.pop()

        for node in list(self.graph.keys()):
            visit(node, [])
        
        return cycles

if __name__ == "__main__":
    analyzer = DependencyAnalyzer(Path(__file__).parent.parent)
    analyzer.build_graph()
    cycles = analyzer.find_cycles()
    
    print("\n" + "="*60)
    print("CIRCULAR DEPENDENCY ANALYSIS")
    print("="*60)
    if cycles:
        print(f"Detected {len(cycles)} circular dependencies:")
        for cycle in cycles:
            print(f" -> ".join(cycle))
    else:
        print("No circular dependencies detected.")
    print("="*60)
