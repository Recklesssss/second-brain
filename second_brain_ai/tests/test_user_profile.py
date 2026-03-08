from core.user_profile import UserProfileService


def test_user_profile_initialization():
    service = UserProfileService()
    assert service is not None


def test_create_user_method_exists():
    service = UserProfileService()
    assert hasattr(service, "create_user")


def test_get_user_method_exists():
    service = UserProfileService()
    assert hasattr(service, "get_user")


def test_add_preference_method_exists():
    service = UserProfileService()
    assert hasattr(service, "add_preference")


def test_add_skill_method_exists():
    service = UserProfileService()
    assert hasattr(service, "add_skill")


def test_add_learning_goal_method_exists():
    service = UserProfileService()
    assert hasattr(service, "add_learning_goal")