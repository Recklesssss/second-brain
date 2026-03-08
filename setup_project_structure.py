# setup_project_structure.py

import os

BASE_DIR = "second_brain_ai"

directories = [
    "backend",
    "api",
    "agents",
    "core",
    "services",
    "database",
    "frontend/react_app",
    "config",
    "build_system",
    "logs/ai_build",
    "logs/errors",
    "logs/metrics",
    "tests"
]

init_files = [
    "api",
    "agents",
    "core",
    "services",
    "database"
]


def create_structure():
    os.makedirs(BASE_DIR, exist_ok=True)

    for directory in directories:
        path = os.path.join(BASE_DIR, directory)
        os.makedirs(path, exist_ok=True)

    for module in init_files:
        init_path = os.path.join(BASE_DIR, module, "__init__.py")
        with open(init_path, "w") as f:
            f.write("")

    print("Project structure created successfully.")


if __name__ == "__main__":
    create_structure()