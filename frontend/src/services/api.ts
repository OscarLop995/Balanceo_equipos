import type {
  Jugador,
  JugadorActualizar,
  JugadorCrear,
} from "../types/jugador";
import type { ResultadoBalanceo, SolicitudBalanceo } from "../types/partido";

const URL_BASE_API = (import.meta.env.VITE_API_URL ?? "/api").replace(
  /\/$/,
  "",
);

/**
 * Error de comunicación con la API.
 *
 * `mensajeServidor` solo contiene texto cuando el backend devolvió un
 * `detail` de tipo string: son mensajes de negocio pensados para el
 * usuario (p. ej. "No existe un jugador con el identificador 5.").
 * Los errores de validación de Pydantic (listas) y los fallos de red
 * nunca se exponen tal cual.
 */
export class ApiError extends Error {
  readonly estado: number | null;
  readonly mensajeServidor: string | null;

  constructor(
    mensaje: string,
    estado: number | null,
    mensajeServidor: string | null,
  ) {
    super(mensaje);
    this.name = "ApiError";
    this.estado = estado;
    this.mensajeServidor = mensajeServidor;
  }
}

function extraerDetalle(cuerpo: unknown): string | null {
  if (
    typeof cuerpo === "object" &&
    cuerpo !== null &&
    "detail" in cuerpo &&
    typeof cuerpo.detail === "string"
  ) {
    return cuerpo.detail;
  }

  return null;
}

async function solicitar<T>(ruta: string, opciones?: RequestInit): Promise<T> {
  let respuesta: Response;

  try {
    respuesta = await fetch(`${URL_BASE_API}${ruta}`, {
      ...opciones,
      headers: {
        Accept: "application/json",
        ...(opciones?.body ? { "Content-Type": "application/json" } : {}),
        ...opciones?.headers,
      },
    });
  } catch (error) {
    throw new ApiError(
      `No se pudo conectar con la API: ${String(error)}`,
      null,
      null,
    );
  }

  const cuerpo: unknown = await respuesta.json().catch(() => null);

  if (!respuesta.ok) {
    throw new ApiError(
      `La API respondió ${respuesta.status} en ${ruta}`,
      respuesta.status,
      extraerDetalle(cuerpo),
    );
  }

  return cuerpo as T;
}

export function obtenerJugadores(): Promise<Jugador[]> {
  return solicitar<Jugador[]>("/jugadores");
}

export function crearJugador(datos: JugadorCrear): Promise<Jugador> {
  return solicitar<Jugador>("/jugadores", {
    method: "POST",
    body: JSON.stringify(datos),
  });
}

export function actualizarJugador(
  idJugador: number,
  datos: JugadorActualizar,
): Promise<Jugador> {
  return solicitar<Jugador>(`/jugadores/${idJugador}`, {
    method: "PUT",
    body: JSON.stringify(datos),
  });
}

export function balancearPartido(
  solicitud: SolicitudBalanceo,
): Promise<ResultadoBalanceo> {
  return solicitar<ResultadoBalanceo>("/partidos/balancear", {
    method: "POST",
    body: JSON.stringify(solicitud),
  });
}
