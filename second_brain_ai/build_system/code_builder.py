import os
from typing import Dict, List, Any


class CodeBuilder:
    """
    CodeBuilder is responsible for generating code artifacts for a given task.

    In the autonomous build loop it receives tasks produced by the TaskGenerator
    and prepares the file outputs defined by the build graph.

    This implementation focuses on deterministic file preparation and
    validation of output paths before code generation.
    """

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root

    def _resolve_path(self, relative_path: str) -> str:
        """
        Resolve a project relative path.
        """
        return os.path.join(self.workspace_root, relative_path)

    def ensure_directory(self, file_path: str) -> None:
        """
        Ensure directory exists for file output.
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def write_file(self, path: str, content: str) -> None:
        """
        Write file safely with directory creation.
        """
        absolute = self._resolve_path(path)
        self.ensure_directory(absolute)

        with open(absolute, "w", encoding="utf-8") as f:
            f.write(content)

    def generate_files(self, outputs: List[Dict[str, Any]]) -> List[str]:
        """
        Generate files defined in the outputs specification.

        outputs format example:

        [
            {
                "path": "module/file.py",
                "content": "..."
            }
        ]
        """
        created_files = []

        for item in outputs:
            path = item["path"]
            content = item["content"]

            self.write_file(path, content)
            created_files.append(path)

        return created_files

    def validate_outputs(self, outputs: List[Dict[str, Any]]) -> bool:
        """
        Validate output specification before writing files.
        """
        for item in outputs:
            if "path" not in item:
                raise ValueError("Output missing 'path'")
            if "content" not in item:
                raise ValueError("Output missing 'content'")

        return True