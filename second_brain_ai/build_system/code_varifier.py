import subprocess
import sys
from typing import Dict, Any, List


class CodeVerifier:
    """
    CodeVerifier validates generated code before commits.

    Verification stages:

    1. Python syntax validation
    2. Import validation
    3. Test execution
    """

    def verify_syntax(self, file_paths: List[str]) -> bool:
        """
        Check Python syntax using the compile step.
        """
        for path in file_paths:
            if not path.endswith(".py"):
                continue

            try:
                with open(path, "r", encoding="utf-8") as f:
                    source = f.read()

                compile(source, path, "exec")

            except SyntaxError as e:
                raise SyntaxError(f"Syntax error in {path}: {e}")

        return True

    def verify_imports(self, modules: List[str]) -> bool:
        """
        Attempt importing modules to ensure dependencies resolve.
        """
        for module in modules:
            try:
                __import__(module)
            except Exception as e:
                raise ImportError(f"Import failed for {module}: {e}")

        return True

    def run_tests(self) -> bool:
        """
        Execute pytest suite.
        """
        result = subprocess.run(
            [sys.executable, "-m", "pytest"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Test execution failed:\n"
                + result.stdout
                + "\n"
                + result.stderr
            )

        return True

    def verify(self, files: List[str], modules: List[str]) -> Dict[str, Any]:
        """
        Perform full verification pipeline.
        """
        self.verify_syntax(files)
        self.verify_imports(modules)
        self.run_tests()

        return {
            "status": "verified",
            "files_checked": files,
            "modules_checked": modules
        }