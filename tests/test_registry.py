from pathlib import Path

from builder.domain.project import Project
from builder.infrastructure.registry_store import RegistryStore
from builder.services.registry_service import RegistryService


def test_register_and_list_project(tmp_path):
    registry_path = tmp_path / "projects.json"
    service = RegistryService(RegistryStore(str(registry_path)))

    project = Project(
        name="Kairos Builder Enterprise",
        path="C:\\KairosBuilderEnterprise",
    )

    service.register(project)

    projects = service.list_projects()

    assert len(projects) == 1
    assert projects[0].name == "Kairos Builder Enterprise"
    assert projects[0].path == "C:\\KairosBuilderEnterprise"


def test_find_project(tmp_path):
    registry_path = tmp_path / "projects.json"
    service = RegistryService(RegistryStore(str(registry_path)))

    service.register(Project(name="Kairos DB Collector", path="C:\\KairosDBCollector"))

    project = service.find("Kairos DB Collector")

    assert project is not None
    assert project.name == "Kairos DB Collector"


def test_remove_project(tmp_path):
    registry_path = tmp_path / "projects.json"
    service = RegistryService(RegistryStore(str(registry_path)))

    service.register(Project(name="ERP", path="C:\\ERP"))

    removed = service.remove("ERP")

    assert removed is True
    assert service.find("ERP") is None


def test_validate_project(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    manifest_path = project_dir / "builder.manifest.json"
    manifest_path.write_text("{}", encoding="utf-8")

    registry_path = tmp_path / "projects.json"
    service = RegistryService(RegistryStore(str(registry_path)))

    service.register(Project(name="Test Project", path=str(project_dir)))

    results = service.validate()

    assert results[0]["name"] == "Test Project"
    assert results[0]["path_exists"] is True
    assert results[0]["manifest_exists"] is True
    assert results[0]["enabled"] is True
