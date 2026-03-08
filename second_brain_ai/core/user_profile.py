from core.memory_system import MemoryStorageService
from core.logging.logger import LoggerFactory


class UserProfileService:
    """
    Manages persistent user profiles and learning preferences.
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("user_profile")
        self.memory = MemoryStorageService()

    def create_user(self, user_id: str, properties: dict):
        """
        Create a new user node.
        """
        properties["user_id"] = user_id
        result = self.memory.store_memory("User", properties)

        self.logger.info(f"User profile created: {user_id}")
        return result

    def get_user(self, user_id: str):
        """
        Retrieve user profile by user_id.
        """
        query = """
        MATCH (u:User {user_id: $user_id})
        RETURN u
        """

        result = self.memory.search_memory(query, {"user_id": user_id})

        if result:
            return result[0]["u"]

        return None

    def add_preference(self, user_id: str, preference: dict):
        """
        Add a preference node linked to the user.
        """
        pref_node = self.memory.store_memory("Preference", preference)

        self.memory.link_memory(
            "User",
            user_id,
            "Preference",
            preference.get("id", ""),
            "HAS_PREFERENCE"
        )

        return pref_node

    def add_skill(self, user_id: str, skill: dict):
        """
        Link a skill node to the user.
        """
        skill_node = self.memory.store_memory("Skill", skill)

        self.memory.link_memory(
            "User",
            user_id,
            "Skill",
            skill.get("id", ""),
            "HAS_SKILL"
        )

        return skill_node

    def add_learning_goal(self, user_id: str, goal: dict):
        """
        Add a learning goal to the user profile.
        """
        goal_node = self.memory.store_memory("LearningGoal", goal)

        self.memory.link_memory(
            "User",
            user_id,
            "LearningGoal",
            goal.get("id", ""),
            "HAS_GOAL"
        )

        return goal_node