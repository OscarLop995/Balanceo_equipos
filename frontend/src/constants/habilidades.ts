import type { Habilidades, NombreHabilidad } from "../types/jugador";

// Solo organización visual y etiquetas. El peso de cada habilidad en la
// puntuación vive exclusivamente en el backend.

export const VALOR_MINIMO_HABILIDAD = 0;
export const VALOR_MAXIMO_HABILIDAD = 100;
export const VALOR_INICIAL_HABILIDAD = 50;

export interface CategoriaHabilidades {
  id: string;
  titulo: string;
  habilidades: readonly NombreHabilidad[];
}

export const CATEGORIAS_HABILIDADES: readonly CategoriaHabilidades[] = [
  {
    id: "fisico",
    titulo: "Físico",
    habilidades: [
      "velocidad",
      "aceleracion",
      "resistencia",
      "fuerza",
      "agilidad",
      "equilibrio",
      "salto",
    ],
  },
  {
    id: "ataque",
    titulo: "Ataque",
    habilidades: [
      "potencia_tiro",
      "precision_tiro",
      "posicionamiento_ofensivo",
      "desmarque",
    ],
  },
  {
    id: "pase",
    titulo: "Pase y creación",
    habilidades: [
      "pase_corto",
      "pase_largo",
      "centros",
      "vision_juego",
      "toma_decisiones",
    ],
  },
  {
    id: "tecnica",
    titulo: "Técnica",
    habilidades: ["control_balon", "regate", "seguridad_balon"],
  },
  {
    id: "defensa",
    titulo: "Defensa",
    habilidades: [
      "marcaje",
      "entradas",
      "intercepciones",
      "posicionamiento_defensivo",
      "anticipacion",
    ],
  },
  {
    id: "portero",
    titulo: "Portero",
    habilidades: ["reflejos", "estirada", "juego_aereo"],
  },
];

export const ETIQUETAS_HABILIDADES: Record<NombreHabilidad, string> = {
  velocidad: "Velocidad",
  aceleracion: "Aceleración",
  resistencia: "Resistencia",
  fuerza: "Fuerza",
  agilidad: "Agilidad",
  equilibrio: "Equilibrio",
  salto: "Salto",
  potencia_tiro: "Potencia de tiro",
  precision_tiro: "Precisión de tiro",
  pase_corto: "Pase corto",
  pase_largo: "Pase largo",
  centros: "Centros",
  control_balon: "Control de balón",
  regate: "Regate",
  vision_juego: "Visión de juego",
  toma_decisiones: "Toma de decisiones",
  marcaje: "Marcaje",
  entradas: "Entradas",
  intercepciones: "Intercepciones",
  posicionamiento_defensivo: "Posicionamiento defensivo",
  posicionamiento_ofensivo: "Posicionamiento ofensivo",
  desmarque: "Desmarque",
  anticipacion: "Anticipación",
  reflejos: "Reflejos",
  estirada: "Estirada",
  juego_aereo: "Juego aéreo",
  seguridad_balon: "Seguridad con el balón",
};

export const NOMBRES_HABILIDADES = Object.keys(
  ETIQUETAS_HABILIDADES,
) as NombreHabilidad[];

export function crearHabilidadesIniciales(): Habilidades {
  return Object.fromEntries(
    NOMBRES_HABILIDADES.map((nombre) => [nombre, VALOR_INICIAL_HABILIDAD]),
  ) as unknown as Habilidades;
}
