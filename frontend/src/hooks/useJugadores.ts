import { useCallback, useEffect, useState } from "react";

import { obtenerJugadores } from "../services/api";
import type { Jugador } from "../types/jugador";
import { mensajeParaUsuario } from "../utils/errores";

type EstadoJugadores =
  | { tipo: "cargando" }
  | { tipo: "error"; mensaje: string }
  | { tipo: "listo"; jugadores: Jugador[] };

export function useJugadores() {
  const [estado, setEstado] = useState<EstadoJugadores>({ tipo: "cargando" });
  const [intento, setIntento] = useState(0);

  useEffect(() => {
    let cancelado = false;

    setEstado({ tipo: "cargando" });

    obtenerJugadores()
      .then((jugadores) => {
        if (!cancelado) {
          setEstado({ tipo: "listo", jugadores });
        }
      })
      .catch((error: unknown) => {
        if (!cancelado) {
          setEstado({
            tipo: "error",
            mensaje: mensajeParaUsuario(
              error,
              "No fue posible cargar los jugadores. Intenta nuevamente.",
            ),
          });
        }
      });

    return () => {
      cancelado = true;
    };
  }, [intento]);

  const recargar = useCallback(() => setIntento((n) => n + 1), []);

  return { estado, recargar };
}
