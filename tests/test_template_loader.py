from builder.services.template_loader import TemplateLoader


def test_load_domain_template():
    loader = TemplateLoader()

    template = loader.load(
        language="python",
        profile="standard",
        template="domain.tpl",
    )

    assert "{{ name }}" in template
