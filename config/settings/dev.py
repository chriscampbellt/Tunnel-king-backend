from .base import *  # noqa

# -----------------------------------------------------------------------------
# Django Debug Toolbar and Django Extensions
# -----------------------------------------------------------------------------
DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]  # noqa
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda x: True}
