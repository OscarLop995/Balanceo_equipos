// Reflejo de los schemas Pydantic en
// src/balanceador_equipos/backend/schemas/jugadores.py

export type Posicion =
  | "portero"
  | "defensa"
  | "mediocampista"
  | "extremo"
  | "delantero";

export interface Habilidades {
  velocidad: number;
  aceleracion: number;
  resistencia: number;
  fuerza: number;
  agilidad: number;
  equilibrio: number;
  salto: number;
  potencia_tiro: number;
  precision_tiro: number;
  pase_corto: number;
  pase_largo: number;
  centros: number;
  control_balon: number;
  regate: number;
  vision_juego: number;
  toma_decisiones: number;
  marcaje: number;
  entradas: number;
  intercepciones: number;
  posicionamiento_defensivo: number;
  posicionamiento_ofensivo: number;
  desmarque: number;
  anticipacion: number;
  reflejos: number;
  estirada: number;
  juego_aereo: number;
  seguridad_balon: number;
}

export type NombreHabilidad = keyof Habilidades;

/** Respuesta de GET /jugadores, POST /jugadores y PUT /jugadores/{id}. */
export interface Jugador {
  id: number;
  nombre: string;
  habilidades: Habilidades;
  /** Calculada por el backend. Solo lectura. */
  posicion_sugerida: Posicion;
  /** Calculada por el backend. Solo lectura. */
  puntuacion: number;
}

/** Cuerpo de POST /jugadores. */
export interface JugadorCrear {
  nombre: string;
  habilidades: Habilidades;
}

/** Cuerpo de PUT /jugadores/{id_jugador}. */
export interface JugadorActualizar {
  nombre: string;
  habilidades: Habilidades;
}
