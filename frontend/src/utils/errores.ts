import { ApiError } from "../services/api";

/**
 * Convierte cualquier error en un mensaje apto para el usuario.
 *
 * Solo se muestran los mensajes de negocio del backend en respuestas
 * 4xx; todo lo demás (red, 5xx, validaciones internas) se reemplaza
 * por el mensaje amigable indicado.
 */
export function mensajeParaUsuario(
  error: unknown,
  mensajePorDefecto: string,
): string {
  if (!(error instanceof ApiError)) {
    return mensajePorDefecto;
  }

  if (error.estado === null) {
    return "No fue posible conectar con el servidor. Verifica que la API esté en ejecución e intenta nuevamente.";
  }

  if (
    error.estado >= 400 &&
    error.estado < 500 &&
    error.mensajeServidor
  ) {
    return error.mensajeServidor;
  }

  return mensajePorDefecto;
}
