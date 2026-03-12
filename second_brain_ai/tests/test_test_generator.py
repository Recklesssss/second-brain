from build_system.test_generator import TestGenerator


def test_generate_import_test():

    generator = TestGenerator()

    content = generator.generate_import_test("module/example.py")

    assert "importlib.import_module" in content
    assert "module.example" in content


def test_generate_file_tests():

    generator = TestGenerator()

    files = [
        "service/module_a.py",
        "service/module_b.py"
    ]

    tests = generator.generate_file_tests(files)

    assert "tests/test_module_a.py" in tests
    assert "tests/test_module_b.py" in tests


def test_build_test_suite():

    generator = TestGenerator()

    outputs = generator.build_test_suite([
        "module/sample.py"
    ])

    assert outputs[0]["path"] == "tests/test_sample.py"
    assert "importlib.import_module" in outputs[0]["content"]