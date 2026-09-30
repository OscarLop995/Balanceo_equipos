import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { EncabezadoPagina } from "../components/EncabezadoPagina";
import {
  EstadoCargando,
  EstadoError,
  EstadoVacio,
  Spinner,
} from "../components/Estados";
import { IconoAlerta, IconoBalon, IconoJugadores, IconoMas } from "../components/Iconos";
import { JugadorSeleccionable } from "../components/JugadorSeleccionable";
import { SelectorTamano } from "../components/SelectorTamano";
import { jugadoresRequeridos, TAMANOS_EQUIPO } from "../constants/partido";
import { useJugadores } from "../hooks/useJugadores";
import { useNotificaciones } from "../hooks/useNotificaciones";
import { balancearPartido } from "../services/api";
import type { Jugador } from "../types/jugador";
import type { TamanoEquipo } from "../types/partido";
import { mensajeParaUsuario } from "../utils/errores";
import type { EstadoResultado } from "./ResultadoPage";
import estilos from "./NuevoPartidoPage.module.css";

export function NuevoPartidoPage() {
  const { estado, recargar } = useJugadores();
  const [tamano, setTamano] = useState<TamanoEquipo>(TAMANOS_EQUIPO[0] ?? 8);
  const [seleccion, setSeleccion] = useState<ReadonlySet<number>>(new Set());
  const [enviando, setEnviando] = useState(false);

  const requeridos = jugadoresRequeridos(tamano);

  return (
    <>
      <EncabezadoPagina
        volverA={{ ruta: "/", texto: "Inicio" }}
        etiqueta="Paso 1 · Formato"
        titulo="Nuevo partido"
        subtitulo="Elige el tamaño de los equipos y selecciona a los jugadores convocados."
      >
        <div className={estilos.selector}>
          <SelectorTamano
            valor={tamano}
            deshabilitado={enviando}
            alCambiar={setTamano}
          />
        </div>
      </EncabezadoPagina>

      <div className="contenedor">
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
              descripcion="Registra jugadores para poder armar un partido."
              accion={
                <Link to="/jugadores/nuevo" className="boton boton--oscuro">
                  <IconoMas />
                  Registrar jugador
                </Link>
              }
            />
          ) : (
            <Convocatoria
              jugadores={estado.jugadores}
              tamano={tamano}
              requeridos={requeridos}
              seleccion={seleccion}
              enviando={enviando}
              alCambiarSeleccion={setSeleccion}
              alCambiarEnviando={setEnviando}
            />
          ))}
      </div>
    </>
  );
}

interface PropsConvocatoria {
  jugadores: Jugador[];
  tamano: TamanoEquipo;
  requeridos: number;
  seleccion: ReadonlySet<number>;
  enviando: boolean;
  alCambiarSeleccion: (seleccion: ReadonlySet<number>) => void;
  alCambiarEnviando: (enviando: boolean) => void;
}

function Convocatoria({
  jugadores,
  tamano,
  requeridos,
  seleccion,
  enviando,
  alCambiarSeleccion,
  alCambiarEnviando,
}: PropsConvocatoria) {
  const navegar = useNavigate();
  const { notificar } = useNotificaciones();
  const [errorServidor, setErrorServidor] = useState<string | null>(null);

  const seleccionados = seleccion.size;
  const completo = seleccionados === requeridos;
  const lleno = seleccionados >= requeridos;
  const sobrantes = seleccionados - requeridos;
  const faltanRegistrados = jugadores.length < requeridos;
  const progreso = Math.min(100, (seleccionados / requeridos) * 100);

  function alternar(idJugador: number) {
    const nueva = new Set(seleccion);

    if (nueva.has(idJugador)) {
      nueva.delete(idJugador);
    } else {
      nueva.add(idJugador);
    }

    alCambiarSeleccion(nueva);
  }

  async function armarEquipos() {
    if (!completo) {
      return;
    }

    alCambiarEnviando(true);
    setErrorServidor(null);

    try {
      // Se respeta el orden de la lista para que la petición sea estable.
      const ids = jugadores
        .map((jugador) => jugador.id)
        .filter((id) => seleccion.has(id));

      const resultado = await balancearPartido({
        jugadores: ids,
        tamano_equipo: tamano,
      });

      const estadoResultado: EstadoResultado = { resultado, tamano };
      navegar("/partidos/resultado", { state: estadoResultado });
    } catch (error) {
      const mensaje = mensajeParaUsuario(
        error,
        "No fue posible armar los equipos. Intenta nuevamente.",
      );
      setErrorServidor(mensaje);
      notificar({ tipo: "error", titulo: mensaje });
      alCambiarEnviando(false);
    }
  }

  return (
    <div className={estilos.convocatoria}>
      <h2 className={estilos.titulo}>
        <span className={estilos.paso}>Paso 2</span>
        Convocatoria
      </h2>

      {faltanRegistrados && (
        <div className={estilos.aviso} role="note">
          <IconoAlerta />
          <p>
            Para {tamano} vs {tamano} se necesitan {requeridos} jugadores y hay{" "}
            {jugadores.length} registrados.{" "}
            <Link to="/jugadores/nuevo">Registrar más jugadores</Link>
          </p>
        </div>
      )}

      {errorServidor && (
        <div className={`${estilos.aviso} ${estilos.avisoError}`} role="alert">
          <IconoAlerta />
          <p>{errorServidor}</p>
        </div>
      )}

      <div className={estilos.lista} role="group" aria-label="Jugadores disponibles">
        {jugadores.map((jugador) => {
          const seleccionado = seleccion.has(jugador.id);

          return (
            <JugadorSeleccionable
              key={jugador.id}
              jugador={jugador}
              seleccionado={seleccionado}
              deshabilitado={enviando || (lleno && !seleccionado)}
              alAlternar={alternar}
            />
          );
        })}
      </div>

      <div className={estilos.barra}>
        <div className={`contenedor ${estilos.barraInterior}`}>
          <div className={estilos.progreso}>
            <p className={estilos.textoProgreso} aria-live="polite">
              Jugadores seleccionados:{" "}
              <strong className="cifra">
                {seleccionados} / {requeridos}
              </strong>
            </p>
            <div
              className={estilos.pista}
              role="progressbar"
              aria-label="Progreso de la convocatoria"
              aria-valuemin={0}
              aria-valuemax={requeridos}
              aria-valuenow={seleccionados}
            >
              <span
                className={`${estilos.relleno} ${completo ? estilos.rellenoCompleto : ""} ${
                  sobrantes > 0 ? estilos.rellenoExcedido : ""
                }`}
                style={{ width: `${progreso}%` }}
              />
            </div>
            {sobrantes > 0 && (
              <p className={estilos.textoExceso}>
                Quita {sobrantes} {sobrantes === 1 ? "jugador" : "jugadores"}{" "}
                para continuar.
              </p>
            )}
          </div>

          <button
            type="button"
            className={`boton boton--primario ${estilos.botonArmar}`}
            disabled={!completo || enviando}
            onClick={armarEquipos}
          >
            {enviando ? (
              <>
                <Spinner />
                Armando equipos...
              </>
            ) : (
              <>
                <IconoBalon />
                Armar equipos
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
