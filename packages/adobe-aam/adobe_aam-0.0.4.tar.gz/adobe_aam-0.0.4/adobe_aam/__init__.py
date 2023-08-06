import os

# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("datetime",
                     "json",
                     "jwt",
                     "cryptography",
                     "os",
                     "pandas",
                     "requests"
                     )

missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

from .login.login import *
from .traits.traits import *
from .reports.reports import *