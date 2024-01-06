import warnings

from django.conf import settings

warnings.filterwarnings(
    "ignore",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)

settings.FIXTURE_DIRS.append(str(settings.BASE_DIR / "tests/fixtures"))
