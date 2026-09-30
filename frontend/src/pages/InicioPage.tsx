import { Link } from "react-router-dom";

import { EncabezadoPagina } from "../components/EncabezadoPagina";
import {
  EstadoCargando,
  EstadoError,
  EstadoVacio,
} from "../components/Estados";
import { IconoCancha, IconoJugadores, IconoMas } from "../components/Iconos";
import { ListaJugadores } from "../components/ListaJugadores";
import { useJugadores } from "../hooks/useJugadores";
import estilos from "./Paginas.module.css";

export function InicioPage() {
  const { estado, recargar } = useJugadores();

  return (
    <>
      <EncabezadoPagina
        etiqueta="Fútbol · Plantilla"
        titulo="Balanceador de Equipos"
        subtitulo="Forma dos equipos equilibrados a partir de las habilidades de tus jugadores."
        acciones={
          <>
            <Link to="/jugadores/nuevo" className="boton boton--primario">
              <IconoMas />
              Registrar jugador
            </Link>
            <Link to="/partidos/nuevo" className="boton boton--translucido">
              <IconoCancha />
              Nuevo partido
            </Link>
          </>
        }
      />

      <div className="contenedor">
        <section aria-labelledby="titulo-jugadores">
          <div className={estilos.cabeceraSeccion}>
            <h2 id="titulo-jugadores" className={estilos.tituloSeccion}>
              Jugadores registrados
            </h2>
            {estado.tipo === "listo" && estado.jugadores.length > 0 && (
              <span className={`${estilos.contador} cifra`}>
                {estado.jugadores.length}
              </span>
            )}
          </div>

          {estado.tipo === "cargando" && (
            <EstadoCargando mensaje="Cargando jugadores..." />
          )}

          {estado.tipo === "error" && (
            <EstadoError mensaje={estado.mensaje} alReintentar={recargar} />
          )}

          {estado.tipo === "listo" &&
            (estado.jugadores.length === 0 ? (
              <EstadoVacio
                icono={<IconoJugadores />}
                titulo="No hay jugadores registrados."
                descripcion="Registra tu primer jugador para comenzar."
                accion={
                  <Link to="/jugadores/nuevo" className="boton boton--oscuro">
                    <IconoMas />
                    Registrar jugador
                  </Link>
                }
              />
            ) : (
              <ListaJugadores jugadores={estado.jugadores} />
            ))}
        </section>
      </div>
    </>
  );
}
