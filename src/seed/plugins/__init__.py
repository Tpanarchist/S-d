"""Auto-import all plugins in the directory to self-register."""

import importlib
import pkgutil

def autodiscover_plugins():
    package = __name__
    for _, name, _ in pkgutil.iter_modules(__path__):
        importlib.import_module(f"{package}.{name}")

autodiscover_plugins()
