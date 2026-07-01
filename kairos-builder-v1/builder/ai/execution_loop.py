class ExecutionLoop:
    def run(self, steps: list[str], service):
        results = []

        for step in steps:
            if step == "new":
                results.append(service.create_project("AutoProject"))

            elif step == "generate":
                results.append(service.generate("domain", "core"))

            elif step == "verify":
                results.append(service.verify())

            elif step == "build":
                results.append(service.build())

            elif step == "package":
                results.append(service.package())

            elif step == "release":
                results.append(service.release())

            else:
                results.append({"skipped": step})

        return results