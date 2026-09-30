import type { ResultadoEquipo } from "../types/partido";
import { formatearPuntuacion } from "../utils/formato";
import { InsigniaPosicion } from "./InsigniaPosicion";
import estilos from "./TarjetaEquipo.module.css";

interface Props {
  nombre: string;
  variante: "a" | "b";
  equipo: ResultadoEquipo;
}

export function TarjetaEquipo({ nombre, variante, equipo }: Props) {
  return (
    <article
      className={`${estilos.tarjeta} ${variante === "a" ? estilos.a : estilos.b}`}
      aria-label={`${nombre}: ${formatearPuntuacion(equipo.puntuacion_total)} puntos`}
    >
      <header className={estilos.cabecera}>
        <div>
          <p className={estilos.etiqueta}>{nombre}</p>
          <p className={estilos.cantidad}>{equipo.jugadores.length} jugadores</p>
        </div>
        <p className={estilos.puntos}>
          <span className="cifra">
            {formatearPuntuacion(equipo.puntuacion_total)}
          </span>
          <span className={estilos.unidad}>puntos</span>
        </p>
      </header>

      <ol className={estilos.lista}>
        {equipo.jugadores.map((jugador, indice) => (
          <li key={jugador.id} className={estilos.jugador}>
            <span className={`${estilos.dorsal} cifra`} aria-hidden="true">
              {indice + 1}
            </span>
            <span className={estilos.nombre}>{jugador.nombre}</span>
            <InsigniaPosicion posicion={jugador.posicion_sugerida} compacta />
          </li>
        ))}
      </ol>
    </article>
  );
}
