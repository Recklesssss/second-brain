import os

REQUIRED_DIRECTORIES = [
    "system",
    "core",
    "database",
    "services",
    "agents",
    "backend",
    "api",
    "frontend",
    "build_system",
    "tests"
]


def test_project_structure_exists():
    for directory in REQUIRED_DIRECTORIES:
        assert os.path.isdir(directory), f"Missing directory: {directory}"