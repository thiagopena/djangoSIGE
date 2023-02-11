""" Configurações do projeto Django """

from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as dburl

PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_ROOT = PROJECT_ROOT / "djangosige"

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default=[], cast=Csv())

# === CACHE  === #


# === DATABASE === #
DATABASES = {
    "default": config("DATABASE_URL", default="sqlite:///./db.sqlite3", cast=dburl),
}


# === DEBUGGING === #
DEBUG = config("DEBUG", default=False, cast=bool)


# === EMAIL === #
DEFAULT_FROM_EMAIL = ""

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST", default="localhost")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_PORT = config("EMAIL_PORT")

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)

# === ERROR REPORTING === #


# === FILE UPLOADS === #
MEDIA_URL = "media/"

MEDIA_ROOT = PROJECT_ROOT / "media"

# === FORMS === #


# === GLOBALIZATION === #
LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# === HTTP === #
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Middleware para paginas que exigem login
    "djangosige.middleware.LoginRequiredMiddleware",
]

WSGI_APPLICATION = "config.wsgi.application"

# === LOGGING === #


# === MODELS === #
FIXTURE_DIRS = [
    PROJECT_ROOT / "fixtures",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # djangosige apps:
    "djangosige.apps.base",
    "djangosige.apps.login",
    "djangosige.apps.cadastro",
    "djangosige.apps.vendas",
    "djangosige.apps.compras",
    "djangosige.apps.fiscal",
    "djangosige.apps.financeiro",
    "djangosige.apps.estoque",
]

# === SECURITY === #
SECRET_KEY = config("SECRET_KEY")

# === SERIALIZATION === #


# === TEMPLATES === #
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PROJECT_ROOT / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # contexto para a versao do sige
                "djangosige.apps.base.context_version.sige_version",
                # contexto para a foto de perfil do usuario
                "djangosige.apps.login.context_user.foto_usuario",
            ],
        },
    },
]

# === TESTING === #


# === URLS === #
ROOT_URLCONF = "config.urls"

# === Auth === #
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "auth.User"

LOGIN_NOT_REQUIRED = (
    r"^/login/$",
    r"/login/esqueceu/",
    r"/login/trocarsenha/",
    r"/logout/",
)

# === Messages === #


# === Sessions === #
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# === Sites === #


# === Static Files === #
STATIC_URL = "static/"

STATIC_ROOT = PROJECT_ROOT / "staticfiles"

STATICFILES_DIRS = [
    PROJECT_ROOT / "static",
]
