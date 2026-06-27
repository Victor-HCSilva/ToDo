import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SETTINGS_DIR = Path(__file__).resolve().parent

# 2. Navegar para cima até a raiz do projeto
# parent de settings.py -> "core"
# parent de core -> "src"
# parent de src -> raiz do projeto "."
BASE_DIR = SETTINGS_DIR.parent.parent

# 3. Construir o caminho completo até o arquivo .env dentro da pasta .envs
dotenv_path = BASE_DIR / ".envs" / ".env"
print(f"Carregando variáveis de ambiente de: {dotenv_path}")
# 4. Carregar as variáveis de ambiente passando o caminho explicitamente
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    # Opcional: um aviso caso o arquivo não seja encontrado no caminho especificado
    print(f"Aviso: Arquivo .env não encontrado em {dotenv_path}")

BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_URL = "main/login"

LOGOUT_REDIRECT_URL = "create/account"

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = os.getenv("TRUSTED_HOSTS").split(",")

# Bloqueia após 5 tentativas falhas
AXES_FAILURE_LIMIT = 5

# Bloqueia por 1 hora (em segundos) após o limite
# Exemplo: 3600 segundos = 1 hora de inatividade
HOUR = 3600
AXES_COOLOFF_TIME = 200 if DEBUG else int(HOUR / 2)

# O tempo é definido em segundos.


SESSION_COOKIE_AGE = 120 if DEBUG else int(HOUR / 10)

# Isso garante que a sessão expire quando o navegador for fechado
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Isso garante que o Django renove o tempo da sessão a cada requisição
SESSION_SAVE_EVERY_REQUEST = True

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "init",
    "main",
    "agenda",
    "checklist",
    "axes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "init.context_processors.session_timeout_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOWED_ORIGINS = [
    "https://" + host for host in os.getenv("TRUSTED_HOSTS").split(",")
]

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

TIME_ZONE = "America/Sao_Paulo"

LANGUAGE_CODE = "pt-br"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
