import yaml
import os
from typing import Dict, List, Any


class TaskGenerator:
    """
    TaskGenerator is responsible for reading the BUILD_GRAPH and STATE_REGISTRY
    and determining which tasks are ready for execution.

    This agent does NOT execute tasks. It only produces a list of READY tasks
    according to the dependency graph rules.
    """

    def __init__(self, build_graph_path: str, state_registry_path: str):
        self.build_graph_path = build_graph_path
        self.state_registry_path = state_registry_path

        self.build_graph = self._load_yaml(build_graph_path)
        self.state_registry = self._load_yaml(state_registry_path)

    def _load_yaml(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"YAML file not found: {path}")

        with open(path, "r") as f:
            return yaml.safe_load(f)

    def _get_completed_tasks(self) -> List[str]:
        """
        Extract completed task IDs from the state registry.
        """
        task_registry = self.state_registry.get("task_registry", {})
        completed = []

        for task_name, task_data in task_registry.items():
            if task_data.get("status") == "completed":
                completed.append(task_data.get("task_id"))

        return completed

    def _extract_graph_tasks(self) -> List[Dict[str, Any]]:
        """
        Flatten the BUILD_GRAPH structure into a list of tasks.
        """
        tasks = []

        phases = self.build_graph.get("build_phases", {})

        for phase_name, phase_data in phases.items():
            for task in phase_data.get("tasks", []):
                tasks.append(task)

        return tasks

    def _dependencies_satisfied(self, task: Dict[str, Any], completed: List[str]) -> bool:
        deps = task.get("dependencies", [])
        return all(dep in completed for dep in deps)

    def get_ready_tasks(self) -> List[Dict[str, Any]]:
        """
        Return tasks that are READY for execution.
        """
        completed = self._get_completed_tasks()
        all_tasks = self._extract_graph_tasks()

        ready_tasks = []

        for task in all_tasks:
            task_id = task["id"]

            if task_id in completed:
                continue

            if self._dependencies_satisfied(task, completed):
                ready_tasks.append(task)

        ready_tasks.sort(key=lambda t: t["id"])

        return ready_tasks

    def generate_task_queue(self) -> List[str]:
        """
        Return a list of READY task IDs.
        """
        ready_tasks = self.get_ready_tasks()
        return [task["id"] for task in ready_tasks]


if __name__ == "__main__":
    generator = TaskGenerator(
        build_graph_path="AI_BUILD_GRAPH.yaml",
        state_registry_path="AI_STATE_REGISTRY.yaml"
    )

    queue = generator.generate_task_queue()

    print("READY_TASKS:")
    for task_id in queue:
        print(task_id)