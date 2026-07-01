from builder.generator.registry import default_registry


def test_registry_supports_mvvm_generators():
    registry = default_registry()

    assert "page" in registry.names()
    assert "widget" in registry.names()
    assert "viewmodel" in registry.names()
    assert "adapter" in registry.names()
