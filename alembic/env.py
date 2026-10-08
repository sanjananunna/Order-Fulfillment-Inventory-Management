from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.config import settings
from app.database import Base

from app.models.category import Category
from app.models.product import Product
from app.models.role import Role
from app.models.user import User
from app.database import Base
from app.models import User, Role, Category, Product, Warehouse


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata