# Copyright (C) 2021  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from swh.counters.interface import CountersInterface

COUNTERS_IMPLEMENTATIONS = {
    "redis": ".redis.Redis",
    "remote": ".api.client.RemoteCounters",
}


def get_counters(cls: str, **kwargs: Dict[str, Any]) -> CountersInterface:
    """Get an counters object of class `cls` with arguments `args`.

    Args:
        cls: counters's class, either 'local' or 'remote'
        args: dictionary of arguments passed to the
            counters class constructor

    Returns:
        an instance of swh.counters's classes (either local or remote)

    Raises:
        ValueError if passed an unknown counters class.
    """
    class_path = COUNTERS_IMPLEMENTATIONS.get(cls)
    if class_path is None:
        raise ValueError(
            "Unknown counters class `%s`. Supported: %s"
            % (cls, ", ".join(COUNTERS_IMPLEMENTATIONS))
        )

    (module_path, class_name) = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path, package=__package__)
    Counters = getattr(module, class_name)
    return Counters(**kwargs)
