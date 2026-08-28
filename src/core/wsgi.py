import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# 1. Ajuste do caminho para encontrar o 'core'
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

# 2. Define o arquivo de configurações
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()
