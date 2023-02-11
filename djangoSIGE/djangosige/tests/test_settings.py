import os
from django.conf import settings
import warnings


warnings.filterwarnings(
    'ignore', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields',
)

settings.FIXTURE_DIRS.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'fixtures'))
