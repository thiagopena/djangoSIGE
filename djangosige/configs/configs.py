# Configurações da database
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Configuração da base de dados
# DATABASES = {
#     'default': {
#         #
#         #Base de dados utilizada (backend)
#         #Obs: Para o MySQL é necessário o mysqlclient (pip install mysqlclient)
#         #
#         'ENGINE': 'django.db.backends.mysql',
#         #'ENGINE': 'django.db.backends.postgresql',
#         #'ENGINE': 'django.db.backends.sqlite3',
#         #'ENGINE': 'django.db.backends.oracle',

#         #Nome da base de dados
#         'NAME': '',

#         #Usuário
#         'USER':'',

#         #Senha
#         'PASSWORD':'',

#         #Host
#         'HOST':'127.0.0.1',

#         #Port
#         'PORT':'3306',
#     }
# }

#
# Configurações do servidor de email
# Obs: Por enquanto o endereço de email é utilizado apenas para a troca de senha do usuário.
# Endereço de email padrão utilizado
#
DEFAULT_FROM_EMAIL = ''

EMAIL_HOST = 'smtp.gmail.com'  # Gmail
# EMAIL_HOST = 'smtp.live.com' #Hotmail

# Usuário do email padrão
EMAIL_HOST_USER = ''

# Senha do email padrão
EMAIL_HOST_PASSWORD = ''

# Verificar a port utilizada pelo serviço de email
EMAIL_PORT = 587

EMAIL_USE_TLS = True
