import os
import sys
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# ==============================================================================
# 1. IDENTIFICAÇÃO DE CAMINHOS
# ==============================================================================
CURRENT_FILE = Path(__file__).resolve()

# Diretório 'src' (onde estão os apps e o manage.py)
SRC_DIR = CURRENT_FILE.parent.parent

# Diretório RAIZ do projeto (onde ficam .envs, db.sqlite3, static e media)
BASE_DIR = SRC_DIR.parent

# Adiciona 'src' ao sys.path para importação direta de apps internos
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# ==============================================================================
# 2. VARIÁVEIS DE AMBIENTE
# ==============================================================================
DOTENV_PATH = BASE_DIR / ".envs" / ".env"
load_dotenv(DOTENV_PATH)


def get_env_bool(name: str, default: bool = False) -> bool:
    """Converte valores de variáveis de ambiente para booleano."""
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("true", "1", "t", "yes")


def get_env_list(name: str, default: str = "") -> list[str]:
    """Converte strings separadas por vírgula em lista de strings limpas."""
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# ==============================================================================
# 3. SEGURANÇA BÁSICA E HOSTS
# ==============================================================================
DEBUG = get_env_bool("DEBUG", default=False)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-dev-key-substitua-em-producao"
    else:
        raise ValueError("A variável SECRET_KEY precisa estar definida em produção!")

# Hosts permitidos — sem fallback hardcoded de produção.
# Em desenvolvimento, defina ALLOWED_HOSTS no arquivo .envs/.env.
# Em produção, a variável de ambiente ALLOWED_HOSTS DEVE estar definida.
ALLOWED_HOSTS = get_env_list(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost" if DEBUG else "",
)
if not DEBUG and not ALLOWED_HOSTS:
    raise ValueError(
        "A variável ALLOWED_HOSTS precisa estar definida em produção! "
        "Exemplo: ALLOWED_HOSTS=example.com,www.example.com"
    )

# Essencial a partir do Django 4.0 caso use formulários/admin em HTTPS
# Em desenvolvimento, usa fallback local. Em produção, defina via variável de ambiente.
CSRF_TRUSTED_ORIGINS = get_env_list(
    "CSRF_TRUSTED_ORIGINS",
    default="http://127.0.0.1,http://localhost" if DEBUG else "",
)
if not DEBUG and not CSRF_TRUSTED_ORIGINS:
    raise ValueError(
        "A variável CSRF_TRUSTED_ORIGINS precisa estar definida em produção! "
        "Exemplo: CSRF_TRUSTED_ORIGINS=https://example.com"
    )

# ==============================================================================
# 4. APLICAÇÕES INSTALADAS
# ==============================================================================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "axes",
]

LOCAL_APPS = [
    "main",
    "agenda",
    "checklist",
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

# ==============================================================================
# 5. MIDDLEWARES
# ==============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
    "core.middleware.CurrentUserMiddleware",
]

ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# ==============================================================================
# 6. TEMPLATES
# ==============================================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            SRC_DIR / "main" / "templates",
            BASE_DIR / "templates",  # Diretório global opcional
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================================================================
# 7. BANCO DE DADOS
# ==============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================================================================
# 8. AUTENTICAÇÃO E CONTROLE DE ACESSO (DJANGO AXES)
# ==============================================================================
LOGIN_URL = "main:login"
LOGOUT_REDIRECT_URL = "main:create_account"

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Regras do django-axes
AXES_FAILURE_LIMIT = 5
AXES_RESET_ON_SUCCESS = True
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_THRESHOLD_WINDOW = timedelta(hours=24)
AXES_COOLOFF_TIME = timedelta(seconds=200) if DEBUG else timedelta(minutes=30)

# Regras de Sessão
SESSION_COOKIE_AGE = 10000 if DEBUG else int(timedelta(minutes=6).total_seconds())
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# ==============================================================================
# 9. ARQUIVOS ESTÁTICOS E MEDIA
# ==============================================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==============================================================================
# 10. INTERNACIONALIZAÇÃO E FUSO HORÁRIO
# ==============================================================================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# 11. SEGURANÇA AVANÇADA (PRODUÇÃO)
# ==============================================================================
if not DEBUG:
    # Cookies seguros só trafegam via HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Cookies: declarações explícitas de HttpOnly e SameSite
    # SESSION_COOKIE_HTTPONLY=True é o default do Django, mas declarar explicitamente
    # evita surpresas em atualizações de versão.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"
    # CSRF_COOKIE_HTTPONLY não é ativado pois interfere com o mecanismo CSRF padrão do Django.

    # Security headers de produção
    SECURE_CONTENT_TYPE_NOSNIFF = True  # Bloqueia MIME sniffing pelo navegador
    SECURE_REFERRER_POLICY = "same-origin"  # Não vaza URL para domínios externos
    X_FRAME_OPTIONS = "DENY"  # Previne clickjacking via iframe

    # NOTA: SECURE_HSTS_SECONDS e SECURE_SSL_REDIRECT foram intencionalmente
    # OMITIDOS. Ativar sem confirmar que HTTPS está funcionando e que o
    # reverse proxy (PythonAnywhere) está configurado corretamente pode
    # derrubar o site. Ative manualmente após validação:
    # SECURE_HSTS_SECONDS = 31536000
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    # SECURE_SSL_REDIRECT = True

    # Detecção de IP atrás de Proxy Reverso (como PythonAnywhere/Nginx)
    # IMPORTANTE: AXES_PROXY_COUNT=1 pressupõe exatamente 1 proxy confiável (PythonAnywhere)
    # entre o cliente e o Django. Se a infraestrutura mudar, revisar este valor.
    # Não confiar cegamente em X-Forwarded-For se a aplicação puder ser acessada diretamente.
    AXES_PROXY_COUNT = 1
    AXES_META_PRECEDENCE_ORDER = (
        "HTTP_X_FORWARDED_FOR",
        "REMOTE_ADDR",
    )
