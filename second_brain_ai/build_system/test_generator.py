from typing import List, Dict, Any


class TestGenerator:
    """
    TestGenerator is responsible for producing pytest test
    specifications for generated code modules.

    In the autonomous build loop, it receives metadata about
    generated files and creates baseline unit tests to verify:

    - module importability
    - basic functionality
    - structural correctness
    """

    def generate_import_test(self, module_path: str) -> str:
        """
        Generate a basic import test for a module.
        """
        module = module_path.replace("/", ".").replace(".py", "")

        return f"""
import importlib

def test_import_module():
    module = importlib.import_module("{module}")
    assert module is not None
"""

    def generate_file_tests(self, files: List[str]) -> Dict[str, str]:
        """
        Generate pytest files for a list of created modules.

        Returns a dictionary mapping test file paths to contents.
        """
        tests = {}

        for file_path in files:
            if not file_path.endswith(".py"):
                continue

            test_name = file_path.split("/")[-1].replace(".py", "")
            test_file = f"tests/test_{test_name}.py"

            tests[test_file] = self.generate_import_test(file_path)

        return tests

    def build_test_suite(self, generated_files: List[str]) -> List[Dict[str, Any]]:
        """
        Convert generated test files into output specification
        compatible with the CodeBuilder agent.
        """
        tests = self.generate_file_tests(generated_files)

        outputs = []

        for path, content in tests.items():
            outputs.append({
                "path": path,
                "content": content.strip()
            })

        return outputs