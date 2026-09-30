import type { ReactNode } from "react";

import { IconoAlerta, IconoRecargar } from "./Iconos";
import estilos from "./Estados.module.css";

export function Spinner({ etiqueta }: { etiqueta?: string }) {
  return (
    <span className={estilos.spinner} role="status">
      <span className={estilos.giro} aria-hidden="true" />
      {etiqueta && <span className="visualmente-oculto">{etiqueta}</span>}
    </span>
  );
}

export function EstadoCargando({
  mensaje,
  filas = 4,
}: {
  mensaje: string;
  filas?: number;
}) {
  return (
    <div className={estilos.cargando} aria-busy="true">
      <p className={estilos.mensajeCargando} role="status">
        <Spinner />
        {mensaje}
      </p>
      <div className={estilos.esqueletos} aria-hidden="true">
        {Array.from({ length: filas }, (_, i) => (
          <div key={i} className={estilos.esqueleto}>
            <span className={estilos.bloque} style={{ width: "38%" }} />
            <span className={estilos.bloque} style={{ width: "14%" }} />
            <span className={estilos.bloque} style={{ width: "22%" }} />
          </div>
        ))}
      </div>
    </div>
  );
}

export function EstadoError({
  mensaje,
  alReintentar,
}: {
  mensaje: string;
  alReintentar?: () => void;
}) {
  return (
    <div className={`${estilos.panel} ${estilos.error}`} role="alert">
      <IconoAlerta className={estilos.iconoPanel} />
      <p className={estilos.titulo}>{mensaje}</p>
      {alReintentar && (
        <button
          type="button"
          className="boton boton--secundario"
          onClick={alReintentar}
        >
          <IconoRecargar />
          Reintentar
        </button>
      )}
    </div>
  );
}

export function EstadoVacio({
  icono,
  titulo,
  descripcion,
  accion,
}: {
  icono: ReactNode;
  titulo: string;
  descripcion: string;
  accion?: ReactNode;
}) {
  return (
    <div className={estilos.panel}>
      <div className={estilos.iconoVacio}>{icono}</div>
      <p className={estilos.titulo}>{titulo}</p>
      <p className={estilos.descripcion}>{descripcion}</p>
      {accion}
    </div>
  );
}
