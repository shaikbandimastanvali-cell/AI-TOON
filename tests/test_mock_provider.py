from services.mock_provider import MockProvider


def test_mock_provider_is_deterministic_and_complete():
    provider = MockProvider()
    first = provider.generate("Gravity", "English", "Adventure")
    second = provider.generate("Gravity", "English", "Adventure")
    assert first == second
    assert len(first.scenes) == 4
    assert len(first.quiz) == 3
