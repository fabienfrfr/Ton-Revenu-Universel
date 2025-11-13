# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./simulateur.db"
    # ou "postgresql://user:password@postgresserver/db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SESSION_LOCAL = sessionmaker (autocommit = False,
                              autoflush  = False,
                              bind       = engine)

Base = declarative_base()
