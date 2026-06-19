from builder import __version__


def main() -> int:
    print("Kairos Builder Enterprise v" + __version__)
    print("Python Core Bootstrap OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
