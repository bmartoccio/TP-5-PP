from typing import Annotated
from fastapi import HTTPException, Path, Query, APIRouter, Depends
from routers import articulos
from schemas.articulos import LibroSchema, LibroUpdateSchema
from database import get_db
from sqlalchemy.orm import Session
import models

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

@libros_routers.get("/", response_model=list[LibroSchema])
async def get_libros(db : Session = Depends(get_db)) -> list[LibroSchema]:
   return db.query(models.Articulos).all()

@libros_routers.get(
        "/{id}",
        responses=DICT_NOT_FOUND,
        response_model=LibroSchema
        ) 
async def get_libros_id(id: Annotated[int, Path(gt=0, description="El ID debe ser mayor a cero")], db : Session = Depends(get_db)) -> LibroSchema:
    libro_encontrado = db.query(models.Articulos).filter(models.Articulos.id ==id).first()
    if not libro_encontrado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return libro_encontrado



##########################
# METODO POST 
##########################

@libros_routers.post(
        "/",
        response_model=LibroSchema)
async def publicar_libro(nuevo_libro:LibroUpdateSchema, db: Session = Depends(get_db)):
    libro = models.Articulos(
        nombre = nuevo_libro.nombre,
        precio = nuevo_libro.precio,
        activo = nuevo_libro.activo,
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


##########################
# METODOS PUT
##########################
@libros_routers.put("/{id}",responses=DICT_NOT_FOUND, response_model=LibroSchema)
async def editar_libros(
    id:Annotated[int,Path(gt=0)],
    libro_editar:LibroUpdateSchema, db: Session = Depends(get_db)
): 
    libro_obtenido = db.query(models.Articulos).filter(models.Articulos.id == id).first()
    if not libro_obtenido:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro_obtenido.nombre = libro_editar.nombre
    libro_obtenido.precio = libro_editar.precio
    libro_obtenido.activo = libro_editar.activo

    db.commit()
    db.refresh(libro_obtenido)

    return libro_obtenido


##########################
# METODO DELETE
##########################

@libros_routers.delete(
    "/{id}",
    responses = DICT_NOT_FOUND,
    response_model = list[LibroSchema]
)
async def eliminar_libro(
    id:Annotated[int,Path(gt=0)],
    logico:Annotated[bool,Query(description="Indica si se debe eliminar un libro o no")] = True, db: Session = Depends(get_db)) -> list[LibroSchema]: 
    libro_obtenido = db.get(models.Articulos, id)
    if libro_obtenido is not None:
        if logico:
            libro_obtenido.activo = False
        else:
            db.delete(libro_obtenido)
            db.commit()
        return db.query(models.Articulos).all()

    raise HTTPException(status_code=404, detail="Artículo no encontrado")