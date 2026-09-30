import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { EncabezadoPagina } from "../components/EncabezadoPagina";
import { FormularioJugador } from "../components/FormularioJugador";
import { crearHabilidadesIniciales } from "../constants/habilidades";
import { ETIQUETAS_POSICIONES } from "../constants/posiciones";
import { useNotificaciones } from "../hooks/useNotificaciones";
import { crearJugador } from "../services/api";
import type { JugadorCrear } from "../types/jugador";
import { mensajeParaUsuario } from "../utils/errores";
import { formatearPuntuacion } from "../utils/formato";

export function RegistrarJugadorPage() {
  const navegar = useNavigate();
  const { notificar } = useNotificaciones();
  const [enviando, setEnviando] = useState(false);
  const [errorServidor, setErrorServidor] = useState<string | null>(null);
  const [valoresIniciales] = useState<JugadorCrear>(() => ({
    nombre: "",
    habilidades: crearHabilidadesIniciales(),
  }));

  async function registrar(datos: JugadorCrear) {
    setEnviando(true);
    setErrorServidor(null);

    try {
      const jugador = await crearJugador(datos);

      notificar({
        tipo: "exito",
        titulo: "Jugador registrado correctamente.",
        detalle: `${jugador.nombre} · ${ETIQUETAS_POSICIONES[jugador.posicion_sugerida]} · ${formatearPuntuacion(jugador.puntuacion)} puntos`,
      });
      navegar("/");
    } catch (error) {
      setErrorServidor(
        mensajeParaUsuario(
          error,
          "No fue posible registrar el jugador. Intenta nuevamente.",
        ),
      );
      window.scrollTo({ top: 0, behavior: "smooth" });
      setEnviando(false);
    }
  }

  return (
    <>
      <EncabezadoPagina
        volverA={{ ruta: "/", texto: "Jugadores" }}
        etiqueta="Nuevo jugador"
        titulo="Registrar jugador"
        subtitulo="Completa el nombre y las habilidades. El sistema calculará su puntuación y posición sugerida."
      />
      <div className="contenedor">
        <FormularioJugador
          valoresIniciales={valoresIniciales}
          textoEnviar="Registrar jugador"
          textoEnviando="Registrando..."
          enviando={enviando}
          errorServidor={errorServidor}
          alEnviar={registrar}
          alCancelar={() => navegar("/")}
        />
      </div>
    </>
  );
}
