from builder.template.engine import TemplateEngine


def test_template_engine():
    engine = TemplateEngine()

    result = engine.render(
        "templates/domain.tpl",
        {
            "class_name": "User",
            "entity_name": "user",
        },
    )

    assert "class User" in result
    assert 'self.name = "user"' in result
