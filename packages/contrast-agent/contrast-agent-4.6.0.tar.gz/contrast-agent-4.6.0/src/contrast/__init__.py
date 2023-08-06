from __future__ import print_function
from pip._vendor.pkg_resources import get_distribution

from contrast.agent.assess.string_tracker import StringTracker
from contrast.utils.context_tracker import ContextTracker

from contrast.extern.six import PY2


__version__ = get_distribution("contrast-agent").version

CS__CONTEXT_TRACKER = ContextTracker()

STRING_TRACKER = StringTracker()


# --- import aliases ---

from contrast.agent.assess.utils import get_properties  # noqa

if PY2:
    from contrast.extern import pathlib2 as pathlib
else:
    import pathlib  # noqa
