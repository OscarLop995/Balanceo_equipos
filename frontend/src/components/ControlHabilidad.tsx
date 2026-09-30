import type { ChangeEvent, CSSProperties } from "react";

import {
  VALOR_MAXIMO_HABILIDAD,
  VALOR_MINIMO_HABILIDAD,
} from "../constants/habilidades";
import estilos from "./ControlHabilidad.module.css";

interface Props {
  id: string;
  etiqueta: string;
  /** Texto tal como lo escribe el usuario (puede estar vacío mientras edita). */
  valor: string;
  error?: string;
  deshabilitado?: boolean;
  alCambiar: (valor: string) => void;
}

export function ControlHabilidad({
  id,
  etiqueta,
  valor,
  error,
  deshabilitado,
  alCambiar,
}: Props) {
  const numero = Number.parseInt(valor, 10);
  const valorSlider = Number.isNaN(numero)
    ? VALOR_MINIMO_HABILIDAD
    : Math.min(VALOR_MAXIMO_HABILIDAD, Math.max(VALOR_MINIMO_HABILIDAD, numero));
  const idError = `${id}-error`;

  function cambiarTexto(evento: ChangeEvent<HTMLInputElement>) {
    // Solo dígitos, máximo 3 caracteres; el rango se valida al enviar.
    alCambiar(evento.target.value.replace(/\D/g, "").slice(0, 3));
  }

  return (
    <div className={`${estilos.control} ${error ? estilos.conError : ""}`}>
      <div className={estilos.cabecera}>
        <label htmlFor={id} className={estilos.etiqueta}>
          {etiqueta}
        </label>
        <input
          id={id}
          className={`${estilos.numero} cifra`}
          type="text"
          inputMode="numeric"
          pattern="[0-9]*"
          autoComplete="off"
          value={valor}
          onChange={cambiarTexto}
          onFocus={(evento) => evento.target.select()}
          disabled={deshabilitado}
          aria-invalid={error ? true : undefined}
          aria-describedby={error ? idError : undefined}
        />
      </div>
      <input
        className={estilos.slider}
        type="range"
        min={VALOR_MINIMO_HABILIDAD}
        max={VALOR_MAXIMO_HABILIDAD}
        step={1}
        value={valorSlider}
        onChange={(evento) => alCambiar(evento.target.value)}
        disabled={deshabilitado}
        aria-label={etiqueta}
        style={{ "--progreso": `${valorSlider}%` } as CSSProperties}
      />
      {error && (
        <p id={idError} className={estilos.error}>
          {error}
        </p>
      )}
    </div>
  );
}
