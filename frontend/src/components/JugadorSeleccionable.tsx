import type { Jugador } from "../types/jugador";
import { IconoCheck } from "./Iconos";
import { InsigniaPosicion } from "./InsigniaPosicion";
import { Puntuacion } from "./Puntuacion";
import estilos from "./JugadorSeleccionable.module.css";

interface Props {
  jugador: Jugador;
  seleccionado: boolean;
  deshabilitado: boolean;
  alAlternar: (idJugador: number) => void;
}

export function JugadorSeleccionable({
  jugador,
  seleccionado,
  deshabilitado,
  alAlternar,
}: Props) {
  return (
    <label
      className={`${estilos.fila} ${seleccionado ? estilos.seleccionado : ""} ${
        deshabilitado ? estilos.deshabilitado : ""
      }`}
    >
      <input
        type="checkbox"
        className="visualmente-oculto"
        checked={seleccionado}
        disabled={deshabilitado}
        onChange={() => alAlternar(jugador.id)}
      />
      <span className={estilos.casilla} aria-hidden="true">
        <IconoCheck />
      </span>
      <span className={estilos.info}>
        <span className={estilos.nombre}>{jugador.nombre}</span>
        <InsigniaPosicion posicion={jugador.posicion_sugerida} />
      </span>
      <Puntuacion valor={jugador.puntuacion} />
    </label>
  );
}
