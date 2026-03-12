import tempfile
import yaml
from build_system.task_generator import TaskGenerator


def create_temp_yaml(data):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml")
    with open(tmp.name, "w") as f:
        yaml.dump(data, f)
    return tmp.name


def test_ready_task_detection():

    build_graph = {
        "build_phases": {
            "phase_test": {
                "tasks": [
                    {
                        "id": "TASK-001",
                        "name": "First Task",
                        "path": "x",
                        "dependencies": []
                    },
                    {
                        "id": "TASK-002",
                        "name": "Second Task",
                        "path": "y",
                        "dependencies": ["TASK-001"]
                    }
                ]
            }
        }
    }

    state_registry = {
        "task_registry": {
            "task1": {
                "task_id": "TASK-001",
                "status": "completed"
            }
        }
    }

    build_graph_file = create_temp_yaml(build_graph)
    state_registry_file = create_temp_yaml(state_registry)

    generator = TaskGenerator(build_graph_file, state_registry_file)

    ready = generator.generate_task_queue()

    assert "TASK-002" in ready


def test_no_ready_tasks_when_dependencies_missing():

    build_graph = {
        "build_phases": {
            "phase_test": {
                "tasks": [
                    {
                        "id": "TASK-002",
                        "name": "Second Task",
                        "path": "y",
                        "dependencies": ["TASK-001"]
                    }
                ]
            }
        }
    }

    state_registry = {"task_registry": {}}

    build_graph_file = create_temp_yaml(build_graph)
    state_registry_file = create_temp_yaml(state_registry)

    generator = TaskGenerator(build_graph_file, state_registry_file)

    ready = generator.generate_task_queue()

    assert ready == []