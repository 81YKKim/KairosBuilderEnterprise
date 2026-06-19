class TemplateRenderer:
    def render(self, template: str, values: dict) -> str:
        content = template

        for key, value in values.items():
            content = content.replace("{{ " + key + " }}", str(value))

        return content
