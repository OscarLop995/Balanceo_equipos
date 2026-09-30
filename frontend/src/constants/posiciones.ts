import type { Posicion } from "../types/jugador";

export const ETIQUETAS_POSICIONES: Record<Posicion, string> = {
  portero: "Portero",
  defensa: "Defensa",
  mediocampista: "Mediocampista",
  extremo: "Extremo",
  delantero: "Delantero",
};

export const ABREVIATURAS_POSICIONES: Record<Posicion, string> = {
  portero: "POR",
  defensa: "DEF",
  mediocampista: "MED",
  extremo: "EXT",
  delantero: "DEL",
};
