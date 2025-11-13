# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

from dataclasses    import dataclass

from sqlalchemy     import Float, Integer, String
from sqlalchemy.orm import MappedColumn, mapped_column

from .database import Base


@dataclass
class Simulation(Base):
    __tablename__ = "simulations"

    id             : MappedColumn[int]   = mapped_column (Integer,
                                                          primary_key = True,
                                                          index       = True)
    revenu_mensuel : MappedColumn[float] = mapped_column (Float)
    statut         : MappedColumn[str]   = mapped_column (String)
    nombre_enfants : MappedColumn[int]   = mapped_column (Integer)
    revenu_de_base : MappedColumn[float] = mapped_column (Float)
    revenu_total   : MappedColumn[float] = mapped_column (Float)
