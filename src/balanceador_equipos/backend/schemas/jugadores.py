from pydantic import BaseModel, Field

from balanceador_equipos.models.posicion import Posicion


class HabilidadesCrear(BaseModel):
    velocidad: int = Field(ge=0, le=100)
    aceleracion: int = Field(ge=0, le=100)
    resistencia: int = Field(ge=0, le=100)
    fuerza: int = Field(ge=0, le=100)
    agilidad: int = Field(ge=0, le=100)
    equilibrio: int = Field(ge=0, le=100)
    salto: int = Field(ge=0, le=100)
    potencia_tiro: int = Field(ge=0, le=100)
    precision_tiro: int = Field(ge=0, le=100)
    pase_corto: int = Field(ge=0, le=100)
    pase_largo: int = Field(ge=0, le=100)
    centros: int = Field(ge=0, le=100)
    control_balon: int = Field(ge=0, le=100)
    regate: int = Field(ge=0, le=100)
    vision_juego: int = Field(ge=0, le=100)
    toma_decisiones: int = Field(ge=0, le=100)
    marcaje: int = Field(ge=0, le=100)
    entradas: int = Field(ge=0, le=100)
    intercepciones: int = Field(ge=0, le=100)
    posicionamiento_defensivo: int = Field(ge=0, le=100)
    posicionamiento_ofensivo: int = Field(ge=0, le=100)
    desmarque: int = Field(ge=0, le=100)
    anticipacion: int = Field(ge=0, le=100)
    reflejos: int = Field(ge=0, le=100)
    estirada: int = Field(ge=0, le=100)
    juego_aereo: int = Field(ge=0, le=100)
    seguridad_balon: int = Field(ge=0, le=100)


class JugadorCrear(BaseModel):
    nombre: str
    habilidades: HabilidadesCrear


class HabilidadesRespuesta(BaseModel):
    velocidad: int
    aceleracion: int
    resistencia: int
    fuerza: int
    agilidad: int
    equilibrio: int
    salto: int
    potencia_tiro: int
    precision_tiro: int
    pase_corto: int
    pase_largo: int
    centros: int
    control_balon: int
    regate: int
    vision_juego: int
    toma_decisiones: int
    marcaje: int
    entradas: int
    intercepciones: int
    posicionamiento_defensivo: int
    posicionamiento_ofensivo: int
    desmarque: int
    anticipacion: int
    reflejos: int
    estirada: int
    juego_aereo: int
    seguridad_balon: int


class JugadorRespuesta(BaseModel):
    id: int
    nombre: str
    habilidades: HabilidadesRespuesta
    posicion_sugerida: Posicion
    puntuacion: float
    
    
class JugadorActualizar(BaseModel):
    nombre: str
    habilidades: HabilidadesCrear