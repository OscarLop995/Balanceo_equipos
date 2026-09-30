// Reflejo de los schemas Pydantic en
// src/balanceador_equipos/backend/schemas/partidos.py

import type { Posicion } from "./jugador";

export type TamanoEquipo = 8 | 9 | 10;

/** Cuerpo de POST /partidos/balancear. */
export interface SolicitudBalanceo {
  jugadores: number[];
  tamano_equipo: TamanoEquipo;
}

export interface JugadorEquipo {
  id: number;
  nombre: string;
  posicion_sugerida: Posicion;
}

export interface ResultadoEquipo {
  jugadores: JugadorEquipo[];
  puntuacion_total: number;
}

/** Respuesta de POST /partidos/balancear. */
export interface ResultadoBalanceo {
  equipo_a: ResultadoEquipo;
  equipo_b: ResultadoEquipo;
  diferencia_puntuacion: number;
}
