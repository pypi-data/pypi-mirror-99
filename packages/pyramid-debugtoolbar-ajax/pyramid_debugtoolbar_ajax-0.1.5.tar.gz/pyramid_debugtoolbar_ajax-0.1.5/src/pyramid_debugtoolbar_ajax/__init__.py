from .panels.ajax import AjaxDebugPanel


__VERSION__ = "0.1.5"


def includeme(config):
    config.add_debugtoolbar_panel(AjaxDebugPanel)
