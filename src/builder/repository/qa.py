from __future__ import annotations

from dataclasses import dataclass

from builder.repository.intelligence import RepositoryIntelligence
from builder.repository.model import PythonModule
from builder.repository.query import RepositoryQuery


@dataclass(frozen=True, slots=True)
class QAIssue:
    code: str
    message: str
    severity: str
    target: str


@dataclass(frozen=True, slots=True)
class QACheckResult:
    name: str
    issues: tuple[QAIssue, ...]
    passed: bool


@dataclass(frozen=True, slots=True)
class QAResult:
    checks: tuple[QACheckResult, ...]
    issue_count: int
    passed: bool
    failed_checks: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RepositoryQA:
    intelligence: RepositoryIntelligence
    query: RepositoryQuery

    CHECK_NAMES = (
        "empty_packages",
        "duplicate_module_names",
        "missing_tests",
        "architecture_rule_violations",
        "generator_rule_violations",
    )

    def run_all(self) -> QAResult:
        checks = tuple(
            self.run_check(name) for name in self.CHECK_NAMES
        )
        issues = tuple(
            issue
            for check in checks
            for issue in check.issues
        )
        failed_checks = tuple(
            check.name for check in checks if not check.passed
        )

        return QAResult(
            checks=checks,
            issue_count=len(issues),
            passed=not failed_checks,
            failed_checks=failed_checks,
        )

    def run_check(
        self,
        name: str,
    ) -> QACheckResult:
        if name == "empty_packages":
            issues = self.empty_packages()
        elif name == "duplicate_module_names":
            issues = self.duplicate_module_names()
        elif name == "missing_tests":
            issues = self.missing_tests()
        elif name == "architecture_rule_violations":
            issues = self.architecture_rule_violations()
        elif name == "generator_rule_violations":
            issues = self.generator_rule_violations()
        else:
            issues = (
                QAIssue(
                    code="repository.unknown_check",
                    message=f"Unknown QA check: {name}",
                    severity="error",
                    target=name,
                ),
            )

        return QACheckResult(
            name=name,
            issues=issues,
            passed=not issues,
        )

    def issues(self) -> tuple[QAIssue, ...]:
        return tuple(
            issue
            for check in self.run_all().checks
            for issue in check.issues
        )

    def passed(self) -> bool:
        return self.run_all().passed

    def empty_packages(self) -> tuple[QAIssue, ...]:
        return tuple(
            QAIssue(
                code="repository.empty_package",
                message=f"Package has no direct modules: {package.name}",
                severity="info",
                target=package.name,
            )
            for package in self.intelligence.empty_packages()
        )

    def duplicate_module_names(self) -> tuple[QAIssue, ...]:
        modules_by_leaf_name: dict[str, list[PythonModule]] = {}

        for module in self._source_modules():
            leaf_name = module.name.rsplit(".", 1)[-1]
            modules_by_leaf_name.setdefault(leaf_name, []).append(module)

        issues = []

        for leaf_name, modules in modules_by_leaf_name.items():
            if len(modules) <= 1:
                continue

            module_names = ", ".join(
                module.name for module in sorted(
                    modules,
                    key=lambda item: item.name,
                )
            )
            issues.append(
                QAIssue(
                    code="repository.duplicate_module_name",
                    message=(
                        "Duplicate module leaf name "
                        f"'{leaf_name}' found in: {module_names}"
                    ),
                    severity="warning",
                    target=leaf_name,
                )
            )

        return tuple(
            sorted(
                issues,
                key=lambda issue: issue.target,
            )
        )

    def missing_tests(self) -> tuple[QAIssue, ...]:
        issues = []

        for module in self._source_modules():
            if self.query.tests_for_module(module.name).count > 0:
                continue

            issues.append(
                QAIssue(
                    code="repository.missing_tests",
                    message=f"Module has no matching test: {module.name}",
                    severity="warning",
                    target=module.name,
                )
            )

        return tuple(
            sorted(
                issues,
                key=lambda issue: issue.target,
            )
        )

    def architecture_rule_violations(self) -> tuple[QAIssue, ...]:
        return ()

    def generator_rule_violations(self) -> tuple[QAIssue, ...]:
        return ()

    def _source_modules(self) -> tuple[PythonModule, ...]:
        return tuple(
            module
            for module in self.intelligence.modules()
            if "tests" not in module.path.parts
        )
