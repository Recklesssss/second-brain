import subprocess
from typing import List


class CommitAgent:
    """
    CommitAgent is responsible for committing generated code to the repository.

    The actual repository permissions are controlled externally by the
    project orchestrator. This agent prepares commits deterministically
    and records commit messages.

    Responsibilities:
    - stage generated files
    - create structured commit messages
    - execute git commit
    """

    def stage_files(self, files: List[str]) -> None:
        """
        Stage files for commit.
        """
        for file in files:
            subprocess.run(["git", "add", file], check=True)

    def create_commit(self, message: str) -> None:
        """
        Execute git commit.
        """
        subprocess.run(
            ["git", "commit", "-m", message],
            check=True
        )

    def commit(self, files: List[str], message: str) -> bool:
        """
        Full commit pipeline.
        """
        self.stage_files(files)
        self.create_commit(message)

        return True