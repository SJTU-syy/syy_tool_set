try:
    from importlib import reload
except ImportError:
    pass
from . import control
from . import ui
reload(control)
reload(ui)
