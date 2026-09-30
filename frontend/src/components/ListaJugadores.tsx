import { Link } from "react-router-dom";

import type { Jugador } from "../types/jugador";
import { IconoEditar } from "./Iconos";
import { InsigniaPosicion } from "./InsigniaPosicion";
import { Puntuacion } from "./Puntuacion";
import estilos from "./ListaJugadores.module.css";

interface Props {
  jugadores: Jugador[];
}

function rutaEdicion(jugador: Jugador): string {
  return `/jugadores/${jugador.id}/editar`;
}

function iniciales(nombre: string): string {
  return nombre
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((parte) => parte[0]?.toUpperCase() ?? "")
    .join("");
}

/**
 * Tabla en escritorio y tarjetas en tablet/móvil. Ambas vistas se
 * renderizan y el CSS muestra la adecuada, sin depender de JS.
 */
export function ListaJugadores({ jugadores }: Props) {
  return (
    <>
      <div className={estilos.contenedorTabla}>
        <table className={estilos.tabla}>
          <thead>
            <tr>
              <th scope="col">Jugador</th>
              <th scope="col">Puntuación</th>
              <th scope="col">Posición sugerida</th>
              <th scope="col">
                <span className="visualmente-oculto">Acciones</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {jugadores.map((jugador) => (
              <tr key={jugador.id}>
                <td>
                  <span className={estilos.nombre}>
                    <span className={estilos.avatar} aria-hidden="true">
                      {iniciales(jugador.nombre)}
                    </span>
                    {jugador.nombre}
                  </span>
                </td>
                <td>
                  <Puntuacion valor={jugador.puntuacion} />
                </td>
                <td>
                  <InsigniaPosicion posicion={jugador.posicion_sugerida} />
                </td>
                <td className={estilos.celdaAccion}>
                  <Link
                    to={rutaEdicion(jugador)}
                    className="boton boton--secundario boton--pequeno"
                    aria-label={`Editar a ${jugador.nombre}`}
                  >
                    <IconoEditar />
                    Editar
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <ul className={estilos.tarjetas}>
        {jugadores.map((jugador) => (
          <li key={jugador.id} className={estilos.tarjeta}>
            <span className={estilos.avatar} aria-hidden="true">
              {iniciales(jugador.nombre)}
            </span>
            <div className={estilos.cuerpoTarjeta}>
              <p className={estilos.nombreTarjeta}>{jugador.nombre}</p>
              <InsigniaPosicion posicion={jugador.posicion_sugerida} />
            </div>
            <div className={estilos.ladoTarjeta}>
              <Puntuacion valor={jugador.puntuacion} />
              <Link
                to={rutaEdicion(jugador)}
                className={estilos.editarTarjeta}
                aria-label={`Editar a ${jugador.nombre}`}
              >
                <IconoEditar />
                <span>Editar</span>
              </Link>
            </div>
          </li>
        ))}
      </ul>
    </>
  );
}
