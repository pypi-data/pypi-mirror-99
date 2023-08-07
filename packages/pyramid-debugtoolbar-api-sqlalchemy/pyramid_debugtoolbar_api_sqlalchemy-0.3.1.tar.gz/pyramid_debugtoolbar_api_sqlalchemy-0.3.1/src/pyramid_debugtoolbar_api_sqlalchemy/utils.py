# pyramid_debugtoolbar
from pyramid_debugtoolbar.panels.sqla import SQLADebugPanel


# ==============================================================================


def get_sqlalchemy_panel(toolbar_panels):
    # PY3 - `toolbar_panels` is a view, not a list
    for panel in toolbar_panels:
        if isinstance(panel, SQLADebugPanel):
            return panel
    return None
