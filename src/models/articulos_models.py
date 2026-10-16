from sqlmodel import SQLModel, Field, Relationship


class AutorBase(SQLModel):
    nombre:str
    cant_libros:int

class Autor(AutorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    articulos: list["Articulos"] = Relationship(back_populates="autor")

class AutorCreate(AutorBase):
    pass

class AutorPublic(AutorBase):
    id:int

class AutorPublicNested(AutorPublic):
    articulos: list["Articulos"] = []

######################################################
class ArticuloBase(SQLModel):
    nombre: str = Field(max_length=90)
    stock: int | None
    precio: int
    activo: bool
    autor_id: int | None = Field(default=None, foreign_key="autor.id")
    


class Articulos(ArticuloBase, table=True):
    id: int| None = Field (default=None, primary_key=True)
    autor: Autor | None = Relationship(back_populates="articulos")

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloPublic(ArticuloBase):
    id:int


class ArticuloPublicNested(ArticuloPublic):
    autor: Autor | None = None
#################################################
