import { formatearPuntuacion } from "../utils/formato";
import estilos from "./Puntuacion.module.css";

interface Props {
  valor: number;
  tamano?: "normal" | "grande";
}

/** Puntuación calculada por el backend, con estilo de marcador. */
export function Puntuacion({ valor, tamano = "normal" }: Props) {
  return (
    <span
      className={`${estilos.puntuacion} ${tamano === "grande" ? estilos.grande : ""}`}
    >
      <span className="cifra">{formatearPuntuacion(valor)}</span>
      <span className={estilos.barra} aria-hidden="true">
        <span
          className={estilos.relleno}
          style={{ width: `${Math.max(0, Math.min(100, valor))}%` }}
        />
      </span>
    </span>
  );
}
