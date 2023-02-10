from alembic.config import Config

from app.settings import settings


alembic_cfg = Config()
alembic_cfg.set_main_option(
    "sqlalchemy.url", settings().SQLALCHEMY_DATABASE_URL
)