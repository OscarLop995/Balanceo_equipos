import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { EncabezadoPagina } from "../components/EncabezadoPagina";
import {
  EstadoCargando,
  EstadoError,
  EstadoVacio,
} from "../components/Estados";
import { FormularioJugador } from "../components/FormularioJugador";
import { IconoJugadores } from "../components/Iconos";
import { InsigniaPosicion } from "../components/InsigniaPosicion";
import { Puntuacion } from "../components/Puntuacion";
import { ETIQUETAS_POSICIONES } from "../constants/posiciones";
import { useJugadores } from "../hooks/useJugadores";
import { useNotificaciones } from "../hooks/useNotificaciones";
import { actualizarJugador } from "../services/api";
import type { Jugador, JugadorActualizar } from "../types/jugador";
import { mensajeParaUsuario } from "../utils/errores";
import { formatearPuntuacion } from "../utils/formato";
import estilos from "./Paginas.module.css";

const VOLVER = { ruta: "/", texto: "Jugadores" };

export function EditarJugadorPage() {
  const { idJugador } = useParams();
  const id = Number(idJugador);
  // La API no expone GET /jugadores/{id}; se busca en el listado.
  const { estado, recargar } = useJugadores();

  if (estado.tipo === "cargando") {
    return (
      <>
        <EncabezadoPagina volverA={VOLVER} titulo="Editar jugador" />
        <div className="contenedor">
          <EstadoCargando mensaje="Cargando jugador..." filas={2} />
        </div>
      </>
    );
  }

  if (estado.tipo === "error") {
    return (
      <>
        <EncabezadoPagina volverA={VOLVER} titulo="Editar jugador" />
        <div className="contenedor">
          <EstadoError
            mensaje="No fue posible cargar el jugador. Intenta nuevamente."
            alReintentar={recargar}
          />
        </div>
      </>
    );
  }

  const jugador = estado.jugadores.find((j) => j.id === id);

  if (!jugador) {
    return (
      <>
        <EncabezadoPagina volverA={VOLVER} titulo="Editar jugador" />
        <div className="contenedor">
          <EstadoVacio
            icono={<IconoJugadores />}
            titulo="No encontramos este jugador."
            descripcion="Es posible que el enlace no sea correcto."
            accion={
              <Link to="/" className="boton boton--oscuro">
                Ver jugadores
              </Link>
            }
          />
        </div>
      </>
    );
  }

  return <EdicionJugador key={jugador.id} jugador={jugador} />;
}

function EdicionJugador({ jugador }: { jugador: Jugador }) {
  const navegar = useNavigate();
  const { notificar } = useNotificaciones();
  const [enviando, setEnviando] = useState(false);
  const [errorServidor, setErrorServidor] = useState<string | null>(null);

  async function guardar(datos: JugadorActualizar) {
    setEnviando(true);
    setErrorServidor(null);

    try {
      const actualizado = await actualizarJugador(jugador.id, datos);

      notificar({
        tipo: "exito",
        titulo: "Jugador actualizado correctamente.",
        detalle: `${actualizado.nombre} · ${ETIQUETAS_POSICIONES[actualizado.posicion_sugerida]} · ${formatearPuntuacion(actualizado.puntuacion)} puntos`,
      });
      navegar("/");
    } catch (error) {
      setErrorServidor(
        mensajeParaUsuario(
          error,
          "No fue posible actualizar el jugador. Intenta nuevamente.",
        ),
      );
      window.scrollTo({ top: 0, behavior: "smooth" });
      setEnviando(false);
    }
  }

  return (
    <>
      <EncabezadoPagina
        volverA={VOLVER}
        etiqueta="Editar jugador"
        titulo={jugador.nombre}
        subtitulo="Modifica el nombre o las habilidades. Si cambian las habilidades, el sistema recalculará la puntuación y la posición."
      />
      <div className="contenedor">
        <FormularioJugador
          valoresIniciales={{
            nombre: jugador.nombre,
            habilidades: jugador.habilidades,
          }}
          textoEnviar="Guardar cambios"
          textoEnviando="Guardando..."
          enviando={enviando}
          errorServidor={errorServidor}
          alEnviar={guardar}
          alCancelar={() => navegar("/")}
          resumen={
            <section className={estilos.resumen} aria-label="Valores calculados">
              <div className={estilos.datoResumen}>
                <span className={estilos.etiquetaResumen}>Puntuación</span>
                <Puntuacion valor={jugador.puntuacion} tamano="grande" />
              </div>
              <div className={estilos.datoResumen}>
                <span className={estilos.etiquetaResumen}>
                  Posición sugerida
                </span>
                <InsigniaPosicion posicion={jugador.posicion_sugerida} />
              </div>
              <p className={estilos.notaResumen}>
                Valores calculados por el sistema. Solo lectura.
              </p>
            </section>
          }
        />
      </div>
    </>
  );
}
