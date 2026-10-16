from typing import Annotated
from fastapi import HTTPException, Path, Query, APIRouter, Depends
from database import get_db
from sqlmodel import Session, select
from models.articulos_models import Articulos,ArticuloPublicNested, ArticuloPublic, ArticuloCreate, ArticuloBase, AutorPublic, AutorCreate, Autor

libros_routers = APIRouter()

DICT_NOT_FOUND: dict = {
    404: {
        "description": "Si el artículo no se encuentra en la lista",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Articulo no encontrado"
                }
            }
        }
        }
    }


##########################
# METODOS GET
##########################

@libros_routers.get("/", response_model=list[ArticuloPublicNested])
async def get_libros(db : Session = Depends(get_db)):
   libros = db.exec(select(Articulos)).all()
   return libros

@libros_routers.get(
        "/{id}",
        responses=DICT_NOT_FOUND,
        response_model=ArticuloPublicNested
        ) 
async def get_libros_id(id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")], db : Session = Depends(get_db)):
    libro_encontrado = db.get(Articulos, id)
    if libro_encontrado is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return libro_encontrado
    



##########################
# METODO POST 
##########################

@libros_routers.post(
        "/",
        response_model=ArticuloPublicNested)
async def publicar_libro(nuevo_libro:ArticuloCreate, db: Session = Depends(get_db)):
    libro = Articulos.model_validate(nuevo_libro)

    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


##########################
# METODOS PUT
##########################
@libros_routers.put("/{id}",responses=DICT_NOT_FOUND, response_model=ArticuloPublic)
async def editar_libros(
    id:Annotated[int,Path(gt=0)],
    libro_editar:ArticuloBase, db: Session = Depends(get_db)
): 
    libro_obtenido = db.get(Articulos, id)
    if libro_obtenido is not None:
        libro_obtenido.nombre = libro_editar.nombre
        libro_obtenido.precio = libro_editar.precio
        libro_obtenido.activo = libro_editar.activo
        libro_obtenido.stock = libro_editar.stock
        libro_obtenido.autor = libro_editar.autor
        db.commit()
        db.refresh(libro_obtenido)
        return libro_obtenido
    raise HTTPException(status_code=404, detail="Libro no encontrado")

##########################
# METODO DELETE
##########################

@libros_routers.delete(
    "/{id}",
    responses = DICT_NOT_FOUND,
    response_model = list[ArticuloPublic]
)
async def eliminar_libro(
    id:Annotated[int,Path(gt=0)],
    logico:Annotated[bool,Query(description="Indica si se debe eliminar un libro o no")] = True, db: Session = Depends(get_db)) -> ArticuloPublic: 
    libro_obtenido = db.get(Articulos, id)
    if libro_obtenido is not None:
        if logico:
            libro_obtenido.activo = False
        else:
            db.delete(libro_obtenido)
            db.commit()
        return db.exec(select(Articulos)).all()

    raise HTTPException(status_code=404, detail="Artículo no encontrado")
########################################################################

@libros_routers.post(
        "/autores",
        tags=["Autores"],
        response_model=AutorPublic)
async def agregar_autor(autor:AutorCreate, db: Session = Depends(get_db)):
    nuevo_autor = Autor.model_validate(autor)

    db.add(nuevo_autor)
    db.commit()
    db.refresh(nuevo_autor)
    return nuevo_autor