import os
import warnings

from djangosige.configs import *

warnings.filterwarnings(
    "ignore",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)

FIXTURE_DIRS.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
)
