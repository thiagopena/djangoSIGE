#!/usr/bin/env python3
"""
Gerador automatizado de arquivo .env para o DjangoSIGE.
Gera uma SECRET_KEY segura e configura valores padrões para desenvolvimento local.
"""

import secrets
from pathlib import Path

# Configuração de caminhos usando Pathlib
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / '.env'

# Caracteres recomendados pelo Django para uma SECRET_KEY segura
CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


def generate_secret_key():
    """Gera uma chave secreta aleatória e segura de 50 caracteres."""
    return ''.join(secrets.choice(CHARS) for _ in range(50))


def create_env_file():
    print("🔍 Verificando ambiente...")
    
    # [PROTEÇÃO]: Evita apagar as configurações atuais do desenvolvedor
    if ENV_FILE.exists():
        print(f"⚠️  Aviso: O arquivo '{ENV_FILE.name}' já existe neste diretório.")
        print("🛑 Operação cancelada para evitar a perda de dados existentes.")
        return

    secret_key = generate_secret_key()

    # Template configurado com valores padrões prontos para rodar localmente (Development)
    config_template = f"""# =============================================================================
# CONFIGURAÇÕES DE AMBIENTE - DJANGOSIGE (AMBIENTE DE DESENVOLVIMENTO)
# =============================================================================

# Ambiente (Mude para False em produção)
DEBUG=True

# Segurança
SECRET_KEY={secret_key}
ALLOWED_HOSTS=127.0.0.1, localhost, .localhost
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Persistência (Padrão: SQLite local para desenvolvimento rápido)
DATABASE_URL=sqlite:///{str(BASE_DIR / 'db.sqlite3')}

# Serviço de E-mail (Padrão: Printa os e-mails enviados direto no terminal)
DEFAULT_FROM_EMAIL=webmaster@localhost
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_USE_TLS=False
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
""".strip()

    try:
        # Grava o arquivo .env de forma limpa usando Pathlib
        ENV_FILE.write_text(config_template, encoding='utf-8')
        print(f"✅ Sucesso: O arquivo '{ENV_FILE.name}' foi gerado com valores padrões de desenvolvimento!")
    except IOError as e:
        print(f"❌ Erro ao criar o arquivo .env: {e}")


if __name__ == '__main__':
    create_env_file()