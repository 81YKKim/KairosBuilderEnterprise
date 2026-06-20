class Context:

    def build(self, name):

        return {
            "name": name,
            "class_name": name.capitalize()
        }