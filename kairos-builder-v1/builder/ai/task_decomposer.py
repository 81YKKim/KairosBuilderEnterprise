class TaskDecomposer:
    def decompose(self, tasks: list[str]) -> list[str]:
        chain = []

        for task in tasks:
            if task == "new":
                chain.append("new default_project")

            elif task == "generate":
                chain.append("generate domain core")

            elif task == "build":
                chain.append("build")

            elif task == "package":
                chain.append("package")

            elif task == "release":
                chain.append("release")

            else:
                chain.append(task)

        return chain