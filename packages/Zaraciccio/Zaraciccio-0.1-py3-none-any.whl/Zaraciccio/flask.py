import pkgutil
import sys


def _wrap_flask(f):
    if f is None:
        return

    from distutils.version import StrictVersion

    if f.__version__ < StrictVersion("1.0"):
        return


if "flask" in sys.modules:
    _wrap_flask(sys.modules["flask"])

else:
    flask_loader = pkgutil.get_loader('flask')
    if flask_loader:
        _exec_module_before = flask_loader.exec_module

        def _exec_module_after(*args, **kwargs):
            _exec_module_before(*args, **kwargs)
            _wrap_flask(sys.modules["flask"])

        flask_loader.exec_module = _exec_module_after
