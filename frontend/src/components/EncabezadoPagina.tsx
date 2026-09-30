import type { ReactNode } from "react";
import { Link } from "react-router-dom";

import { IconoVolver } from "./Iconos";
import estilos from "./EncabezadoPagina.module.css";

interface Props {
  titulo: string;
  subtitulo?: string;
  etiqueta?: string;
  volverA?: { ruta: string; texto: string };
  acciones?: ReactNode;
  children?: ReactNode;
}

/** Banda superior con motivo de cancha, común a todas las páginas. */
export function EncabezadoPagina({
  titulo,
  subtitulo,
  etiqueta,
  volverA,
  acciones,
  children,
}: Props) {
  return (
    <section className={estilos.encabezado}>
      <div className={estilos.lineas} aria-hidden="true" />
      <div className={`contenedor ${estilos.interior}`}>
        {volverA && (
          <Link to={volverA.ruta} className={estilos.volver}>
            <IconoVolver />
            {volverA.texto}
          </Link>
        )}

        <div className={estilos.fila}>
          <div className={estilos.textos}>
            {etiqueta && <p className={estilos.etiqueta}>{etiqueta}</p>}
            <h1 className={estilos.titulo}>{titulo}</h1>
            {subtitulo && <p className={estilos.subtitulo}>{subtitulo}</p>}
          </div>
          {acciones && <div className={estilos.acciones}>{acciones}</div>}
        </div>

        {children}
      </div>
    </section>
  );
}
