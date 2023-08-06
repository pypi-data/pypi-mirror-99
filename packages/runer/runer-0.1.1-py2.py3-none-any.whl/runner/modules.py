import sys
import glob
from os.path import dirname, basename, isfile, join

sys.path.append(join(dirname(__file__), 'modules'))

Modules = {}

DEFAULT_MODULE = "shell"

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# template


def runer(m: dict, cmd, *args, **kwargs):
    return (-1, "", "")


def module_get(**kwargs):
    name = DEFAULT_MODULE
    if "t" in kwargs:
        name = kwargs["t"]
    m = Modules.get(kwargs["t"], dict())
    return m


def getter(name: str):
    if name in Modules:
        return Modules[name].copy()
    return {}


def register(name: str, m: dict):
    Modules[name] = m


def AutoLoadModules():
    global Modules
    global PY2
    global PY3
    modules = glob.glob(join(dirname(__file__), 'modules', '*.py'))
    for f in modules:
        if isfile(f) and not f.endswith('__init__.py'):
            if sys.version < '3':  # python2
                import imp
                lib = imp.load_source(basename(f)[:-3], f)
                if hasattr(lib, 'register_auto'):
                    lib.register_auto(Modules)
            else:
                from importlib import import_module
                lib = __import__(basename(f)[:-3])
                if hasattr(lib, 'register_auto'):
                    lib.register_auto(Modules)
                    # print(Modules)
