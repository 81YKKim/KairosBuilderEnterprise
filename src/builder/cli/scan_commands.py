from builder.services.repository_scanner import RepositoryScanner


def add_scan_commands(subparsers) -> None:
    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("--path", required=True)
    scan_parser.set_defaults(func=handle_scan)


def handle_scan(args) -> None:
    scanner = RepositoryScanner()
    info = scanner.scan(args.path)

    print("Repository")
    print(f"Name           : {info.name}")
    print(f"Path           : {info.path}")
    print(f"Language       : {info.language}")
    print(f"Architecture   : {info.architecture}")
    print(f"Git Found      : {info.git_found}")
    print(f"Branch         : {info.branch}")
    print(f"Manifest Found : {info.manifest_found}")
    print(f"Directories    : {info.directories}")
    print(f"Source Files   : {info.source_files}")
    print(f"Test Files     : {info.test_files}")
