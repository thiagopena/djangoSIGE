import os
from djangosige.configs import *

FIXTURE_DIRS.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'fixtures'))
