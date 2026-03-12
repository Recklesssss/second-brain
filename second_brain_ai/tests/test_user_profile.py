from core.user_profile import UserProfileService


def test_user_profile_service_creation():

    service = UserProfileService()

    assert service is not None


def test_user_profile_methods_exist():

    service = UserProfileService()

    assert hasattr(service, "create_profile")
    assert hasattr(service, "get_profile")
    assert hasattr(service, "update_profile")
    assert hasattr(service, "delete_profile")