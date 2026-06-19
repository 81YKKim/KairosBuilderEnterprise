# Architecture Analyzer Sequence Diagram

```text
User
 │
 ▼
builder analyze --path <repository>
 │
 ▼
CLI
 │
 ▼
ArchitectureAnalyzer
 │
 ▼
Filesystem
 │
 ▼
Package Analyzer
 │
 ▼
Dependency Analyzer
 │
 ▼
Architecture Report
 │
 ▼
Console Output
```
