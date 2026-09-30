import { Link, useLocation } from "react-router-dom";

import { EncabezadoPagina } from "../components/EncabezadoPagina";
import { EstadoVacio } from "../components/Estados";
import { IconoCancha, IconoServidor } from "../components/Iconos";
import { TarjetaEquipo } from "../components/TarjetaEquipo";
import type { ResultadoBalanceo, TamanoEquipo } from "../types/partido";
import { formatearPuntuacion } from "../utils/formato";
import estilos from "./ResultadoPage.module.css";

/** Estado de navegación que NuevoPartidoPage entrega a esta página. */
export interface EstadoResultado {
  resultado: ResultadoBalanceo;
  tamano: TamanoEquipo;
}

function esEstadoResultado(valor: unknown): valor is EstadoResultado {
  if (typeof valor !== "object" || valor === null) {
    return false;
  }

  const posible = valor as Partial<EstadoResultado>;

  return (
    typeof posible.tamano === "number" &&
    typeof posible.resultado === "object" &&
    posible.resultado !== null &&
    Array.isArray(posible.resultado.equipo_a?.jugadores) &&
    Array.isArray(posible.resultado.equipo_b?.jugadores) &&
    typeof posible.resultado.diferencia_puntuacion === "number"
  );
}

export function ResultadoPage() {
  const { state } = useLocation();

  // El resultado no se persiste: si se recarga la página o se entra
  // directamente, se invita a armar un nuevo partido.
  if (!esEstadoResultado(state)) {
    return (
      <>
        <EncabezadoPagina
          volverA={{ ruta: "/", texto: "Inicio" }}
          titulo="Resultado del balanceo"
        />
        <div className="contenedor">
          <EstadoVacio
            icono={<IconoCancha />}
            titulo="No hay un resultado para mostrar."
            descripcion="Los equipos se muestran justo después de armarlos. Crea un nuevo partido para obtener una distribución."
            accion={
              <Link to="/partidos/nuevo" className="boton boton--oscuro">
                Nuevo partido
              </Link>
            }
          />
        </div>
      </>
    );
  }

  const { resultado, tamano } = state;
  const { equipo_a: equipoA, equipo_b: equipoB } = resultado;

  return (
    <>
      <EncabezadoPagina
        volverA={{ ruta: "/", texto: "Inicio" }}
        etiqueta={`${tamano} vs ${tamano}`}
        titulo="Equipos armados"
      >
        <div className={estilos.marcador} aria-label="Marcador de puntuaciones">
          <div className={`${estilos.lado} ${estilos.ladoA}`}>
            <span className={estilos.nombreLado}>Equipo A</span>
            <span className={`${estilos.puntos} cifra`}>
              {formatearPuntuacion(equipoA.puntuacion_total)}
            </span>
          </div>
          <div className={estilos.centro}>
            <span className={estilos.etiquetaDiferencia}>Diferencia</span>
            <span className={`${estilos.diferencia} cifra`}>
              {formatearPuntuacion(resultado.diferencia_puntuacion)}
            </span>
          </div>
          <div className={`${estilos.lado} ${estilos.ladoB}`}>
            <span className={estilos.nombreLado}>Equipo B</span>
            <span className={`${estilos.puntos} cifra`}>
              {formatearPuntuacion(equipoB.puntuacion_total)}
            </span>
          </div>
        </div>
        <p className={estilos.textoDiferencia}>
          Diferencia: {formatearPuntuacion(resultado.diferencia_puntuacion)}{" "}
          puntos
        </p>
      </EncabezadoPagina>

      <div className="contenedor">
        <div className={estilos.origen}>
          <IconoServidor />
          <p>
            Distribución calculada por el algoritmo de balanceo del servidor,
            que busca la menor diferencia de puntuación entre ambos equipos.
          </p>
        </div>

        <div className={estilos.equipos}>
          <TarjetaEquipo nombre="Equipo A" variante="a" equipo={equipoA} />
          <TarjetaEquipo nombre="Equipo B" variante="b" equipo={equipoB} />
        </div>

        <div className={estilos.acciones}>
          <Link to="/" className="boton boton--secundario">
            Volver al inicio
          </Link>
          <Link to="/partidos/nuevo" className="boton boton--oscuro">
            <IconoCancha />
            Nuevo partido
          </Link>
        </div>
      </div>
    </>
  );
}
