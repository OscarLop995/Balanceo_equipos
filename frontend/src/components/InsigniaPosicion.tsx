import {
  ABREVIATURAS_POSICIONES,
  ETIQUETAS_POSICIONES,
} from "../constants/posiciones";
import type { Posicion } from "../types/jugador";
import estilos from "./InsigniaPosicion.module.css";

interface Props {
  posicion: Posicion;
  compacta?: boolean;
}

export function InsigniaPosicion({ posicion, compacta = false }: Props) {
  const etiqueta = ETIQUETAS_POSICIONES[posicion];

  return (
    <span
      className={`${estilos.insignia} ${estilos[posicion]}`}
      title={compacta ? etiqueta : undefined}
    >
      <span className={estilos.punto} aria-hidden="true" />
      {compacta ? (
        <>
          <span aria-hidden="true">{ABREVIATURAS_POSICIONES[posicion]}</span>
          <span className="visualmente-oculto">{etiqueta}</span>
        </>
      ) : (
        etiqueta
      )}
    </span>
  );
}
