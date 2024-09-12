import sys
import pkgutil
import importlib


def import_and_reload_modules(package_name):
    package = sys.modules.get(package_name)
    if package is None:
        raise ValueError(f"Package '{package_name}' is not loaded.")

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        if full_module_name in sys.modules:
            print(f"Reloading module '{full_module_name}'...")
            importlib.reload(sys.modules[full_module_name])
        else:
            print(f"Importing module '{full_module_name}'...")
            importlib.import_module(full_module_name)


import_and_reload_modules('comp')
import_and_reload_modules('func')