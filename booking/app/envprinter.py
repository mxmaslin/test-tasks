import os

envs = ('FLASK_DEBUG', 'API_VERSION', 'SECRET_KEY', 'POSTGRES_HOST', 'POSTGRES_DB', 'POSTGRES_PORT', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'APP_PORT', 'APP_HOST')

for env in envs:
    print(os.environ[env])