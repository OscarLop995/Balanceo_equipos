import { jugadoresRequeridos, TAMANOS_EQUIPO } from "../constants/partido";
import type { TamanoEquipo } from "../types/partido";
import estilos from "./SelectorTamano.module.css";

interface Props {
  valor: TamanoEquipo;
  deshabilitado?: boolean;
  alCambiar: (tamano: TamanoEquipo) => void;
}

export function SelectorTamano({ valor, deshabilitado, alCambiar }: Props) {
  return (
    <fieldset className={estilos.selector} disabled={deshabilitado}>
      <legend className="visualmente-oculto">Tamaño de los equipos</legend>
      {TAMANOS_EQUIPO.map((tamano) => (
        <label
          key={tamano}
          className={`${estilos.opcion} ${valor === tamano ? estilos.activa : ""}`}
        >
          <input
            type="radio"
            name="tamano-equipo"
            className="visualmente-oculto"
            value={tamano}
            checked={valor === tamano}
            onChange={() => alCambiar(tamano)}
          />
          <span className={`${estilos.marcador} cifra`}>
            {tamano}
            <span className={estilos.vs}>vs</span>
            {tamano}
          </span>
          <span className={estilos.total}>
            {jugadoresRequeridos(tamano)} jugadores
          </span>
        </label>
      ))}
    </fieldset>
  );
}
