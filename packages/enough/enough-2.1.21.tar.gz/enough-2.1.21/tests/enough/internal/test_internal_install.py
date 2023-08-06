from enough.internal.cmd import main
from enough.version import __version__


def test_enough_install_script(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    assert main(['--debug', 'install', 'internal/data/install.sh']) == 0
    out, err = capsys.readouterr()
    assert 'docker run' in out
    assert 'libvirt' in out
    assert 'docker.sock' in out
    assert 'function()' not in out
    assert __version__ in out


def test_enough_install_script_no_version(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    assert main(['--debug', 'install', 'internal/data/install.sh', '--no-version']) == 0
    out, err = capsys.readouterr()
    assert 'docker run' in out
    assert 'function()' not in out
    assert __version__ not in out


def test_enough_install_function(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    assert main(['--debug', 'install', '--function', 'internal/data/install.sh']) == 0
    out, err = capsys.readouterr()
    assert 'docker run' in out
    assert 'function enough()' in out
    assert __version__ in out


def test_enough_install_defaults(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    assert main(['--debug', 'install']) == 0
    out, err = capsys.readouterr()
    assert 'docker run' in out
    assert 'function enough()' in out
    assert __version__ in out


def test_enough_install_set_registry(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    registry = 'REGISTRY'
    assert main(['--debug', 'install', 'internal/data/install.sh', '--registry', registry]) == 0
    out, err = capsys.readouterr()
    assert 'docker run' in out
    assert 'function()' not in out
    assert registry in out


def test_enough_install_default_registry(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    assert main(['--debug', 'install', 'internal/data/install.sh']) == 0
    out, err = capsys.readouterr()
    assert 'docker run' in out
    assert 'function()' not in out
    assert 'enoughcommunity/' in out
