from builder.cli.main import main


def test_cli_version():
    assert main(["version"]) == 0


def test_cli_info():
    assert main(["info"]) == 0


def test_cli_doctor():
    assert main(["doctor"]) == 0
