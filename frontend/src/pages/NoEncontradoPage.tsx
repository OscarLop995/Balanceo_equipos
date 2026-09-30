import { Link } from "react-router-dom";

import { EncabezadoPagina } from "../components/EncabezadoPagina";
import { EstadoVacio } from "../components/Estados";
import { IconoBalon } from "../components/Iconos";

export function NoEncontradoPage() {
  return (
    <>
      <EncabezadoPagina titulo="Fuera de juego" />
      <div className="contenedor">
        <EstadoVacio
          icono={<IconoBalon />}
          titulo="La página que buscas no existe."
          descripcion="Vuelve al inicio para seguir gestionando tus jugadores."
          accion={
            <Link to="/" className="boton boton--oscuro">
              Volver al inicio
            </Link>
          }
        />
      </div>
    </>
  );
}
