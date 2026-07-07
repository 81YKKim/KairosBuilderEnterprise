from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from builder.repository.model import (
    PythonModule,
    PythonPackage,
    RepositoryDocumentation,
    RepositoryModel,
    RepositoryStatistics,
    RepositoryTestFile,
)


def test_repository_model_describes_repository_state():
    root = Path("C:/KairosBuilderEnterprise")
    git_root = root

    model = RepositoryModel(
        repository_root=root,
        git_root=git_root,
        branch="main",
        head_commit="09168ec",
        python_modules=(
            PythonModule(
                name="builder.repository.model",
                path=Path("src/builder/repository/model.py"),
                package="builder.repository",
            ),
        ),
        packages=(
            PythonPackage(
                name="builder.repository",
                path=Path("src/builder/repository"),
            ),
        ),
        tests=(
            RepositoryTestFile(
                name="test_repository_model",
                path=Path("tests/test_repository_model.py"),
            ),
        ),
        documentation=(
            RepositoryDocumentation(
                title="Builder X Self Analysis",
                path=Path("docs/builder_x/BUILDER_X_SELF_ANALYSIS.md"),
            ),
        ),
        statistics=RepositoryStatistics(
            directory_count=10,
            file_count=20,
            python_file_count=5,
            test_file_count=1,
            documentation_file_count=1,
            package_count=1,
            module_count=1,
        ),
    )

    assert model.repository_root == root
    assert model.git_root == git_root
    assert model.branch == "main"
    assert model.head_commit == "09168ec"
    assert model.python_modules[0].name == "builder.repository.model"
    assert model.packages[0].name == "builder.repository"
    assert model.tests[0].name == "test_repository_model"
    assert model.documentation[0].title == "Builder X Self Analysis"
    assert model.statistics.python_file_count == 5


def test_repository_model_is_immutable():
    model = RepositoryModel(
        repository_root=Path("repo"),
        git_root=Path("repo"),
        branch="main",
        head_commit="abc123",
        python_modules=(),
        packages=(),
        tests=(),
        documentation=(),
        statistics=RepositoryStatistics(
            directory_count=0,
            file_count=0,
            python_file_count=0,
            test_file_count=0,
            documentation_file_count=0,
            package_count=0,
            module_count=0,
        ),
    )

    with pytest.raises(FrozenInstanceError):
        model.branch = "develop"


def test_repository_model_collections_are_tuple_based():
    model = RepositoryModel(
        repository_root=Path("repo"),
        git_root=Path("repo"),
        branch="main",
        head_commit="abc123",
        python_modules=(),
        packages=(),
        tests=(),
        documentation=(),
        statistics=RepositoryStatistics(
            directory_count=0,
            file_count=0,
            python_file_count=0,
            test_file_count=0,
            documentation_file_count=0,
            package_count=0,
            module_count=0,
        ),
    )

    assert isinstance(model.python_modules, tuple)
    assert isinstance(model.packages, tuple)
    assert isinstance(model.tests, tuple)
    assert isinstance(model.documentation, tuple)
