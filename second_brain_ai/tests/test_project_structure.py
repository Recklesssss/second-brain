import os

BASE_DIR = "second_brain_ai"

required_dirs = [
    "backend",
    "api",
    "agents",
    "core",
    "services",
    "database",
    "frontend",
    "config",
    "build_system",
    "logs",
    "tests"
]

def test_directories_exist():
    for d in required_dirs:
        path = os.path.join(BASE_DIR, d)
        assert os.path.isdir(path), f"{d} directory missing"