from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Articulos(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    precio = Column(Integer)
    activo = Column(Boolean)