import type { TamanoEquipo } from "../types/partido";

// Opciones que acepta el backend (SolicitudBalanceo.tamano_equipo).
export const TAMANOS_EQUIPO: readonly TamanoEquipo[] = [8, 9, 10];

export function jugadoresRequeridos(tamano: TamanoEquipo): number {
  return tamano * 2;
}
