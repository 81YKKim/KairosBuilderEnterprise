# Architecture Analyzer Component Diagram

```text
                User
                  │
                  ▼
                CLI
                  │
                  ▼
        architecture_commands.py
                  │
                  ▼
        ArchitectureAnalyzer
          ┌────────┴────────┐
          ▼                 ▼
 Package Analyzer   Dependency Analyzer
          └────────┬────────┘
                   ▼
        ArchitectureReport
                   │
                   ▼
             Filesystem
```

## Components

### CLI

Receives user commands.

### ArchitectureAnalyzer

Coordinates the architecture analysis.

### Package Analyzer

Detects packages and layers.

### Dependency Analyzer

Collects dependency information.

### ArchitectureReport

Stores analysis results.

### Filesystem

Provides operating system access.
