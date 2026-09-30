import { useState, type FormEvent, type ReactNode } from "react";

import {
  CATEGORIAS_HABILIDADES,
  ETIQUETAS_HABILIDADES,
  NOMBRES_HABILIDADES,
  VALOR_MAXIMO_HABILIDAD,
  VALOR_MINIMO_HABILIDAD,
} from "../constants/habilidades";
import type {
  Habilidades,
  JugadorCrear,
  NombreHabilidad,
} from "../types/jugador";
import { ControlHabilidad } from "./ControlHabilidad";
import { Spinner } from "./Estados";
import { IconoAlerta } from "./Iconos";
import estilos from "./FormularioJugador.module.css";

type TextosHabilidades = Record<NombreHabilidad, string>;
type ErroresHabilidades = Partial<Record<NombreHabilidad, string>>;

interface Props {
  valoresIniciales: JugadorCrear;
  textoEnviar: string;
  textoEnviando: string;
  enviando: boolean;
  errorServidor: string | null;
  /** Contenido de solo lectura mostrado antes del formulario (modo edición). */
  resumen?: ReactNode;
  alEnviar: (datos: JugadorCrear) => void;
  alCancelar: () => void;
}

function aTextos(habilidades: Habilidades): TextosHabilidades {
  return Object.fromEntries(
    NOMBRES_HABILIDADES.map((nombre) => [nombre, String(habilidades[nombre])]),
  ) as TextosHabilidades;
}

function validarHabilidad(texto: string): string | undefined {
  if (texto.trim() === "") {
    return "Introduce un valor.";
  }

  const valor = Number(texto);

  if (
    !Number.isInteger(valor) ||
    valor < VALOR_MINIMO_HABILIDAD ||
    valor > VALOR_MAXIMO_HABILIDAD
  ) {
    return `Debe ser un número entero entre ${VALOR_MINIMO_HABILIDAD} y ${VALOR_MAXIMO_HABILIDAD}.`;
  }

  return undefined;
}

export function FormularioJugador({
  valoresIniciales,
  textoEnviar,
  textoEnviando,
  enviando,
  errorServidor,
  resumen,
  alEnviar,
  alCancelar,
}: Props) {
  const [nombre, setNombre] = useState(valoresIniciales.nombre);
  const [textos, setTextos] = useState<TextosHabilidades>(() =>
    aTextos(valoresIniciales.habilidades),
  );
  const [errorNombre, setErrorNombre] = useState<string>();
  const [errores, setErrores] = useState<ErroresHabilidades>({});

  function cambiarHabilidad(habilidad: NombreHabilidad, texto: string) {
    setTextos((actuales) => ({ ...actuales, [habilidad]: texto }));

    if (errores[habilidad]) {
      setErrores((actuales) => ({
        ...actuales,
        [habilidad]: validarHabilidad(texto),
      }));
    }
  }

  function enviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();

    const nombreLimpio = nombre.trim();
    const nuevoErrorNombre = nombreLimpio
      ? undefined
      : "El nombre del jugador no puede estar vacío.";

    const nuevosErrores: ErroresHabilidades = {};

    for (const habilidad of NOMBRES_HABILIDADES) {
      const error = validarHabilidad(textos[habilidad]);

      if (error) {
        nuevosErrores[habilidad] = error;
      }
    }

    setErrorNombre(nuevoErrorNombre);
    setErrores(nuevosErrores);

    const primerError = nuevoErrorNombre
      ? "nombre"
      : NOMBRES_HABILIDADES.find((h) => nuevosErrores[h]);

    if (primerError) {
      document
        .getElementById(
          primerError === "nombre" ? "campo-nombre" : `habilidad-${primerError}`,
        )
        ?.focus();
      return;
    }

    const habilidades = Object.fromEntries(
      NOMBRES_HABILIDADES.map((h) => [h, Number(textos[h])]),
    ) as unknown as Habilidades;

    alEnviar({ nombre: nombreLimpio, habilidades });
  }

  const cantidadErrores =
    Object.values(errores).filter(Boolean).length + (errorNombre ? 1 : 0);

  return (
    <form className={estilos.formulario} onSubmit={enviar} noValidate>
      {resumen}

      {errorServidor && (
        <div className={estilos.alerta} role="alert">
          <IconoAlerta />
          <p>{errorServidor}</p>
        </div>
      )}

      <section className={estilos.seccion} aria-labelledby="titulo-basica">
        <h2 id="titulo-basica" className={estilos.tituloSeccion}>
          Información básica
        </h2>
        <div className={estilos.campoNombre}>
          <label htmlFor="campo-nombre" className={estilos.etiqueta}>
            Nombre
          </label>
          <input
            id="campo-nombre"
            className={`${estilos.entrada} ${errorNombre ? estilos.entradaError : ""}`}
            type="text"
            autoComplete="off"
            maxLength={80}
            placeholder="Ej.: Juan Pérez"
            value={nombre}
            onChange={(evento) => {
              setNombre(evento.target.value);
              if (errorNombre && evento.target.value.trim()) {
                setErrorNombre(undefined);
              }
            }}
            disabled={enviando}
            aria-invalid={errorNombre ? true : undefined}
            aria-describedby={errorNombre ? "campo-nombre-error" : undefined}
          />
          {errorNombre && (
            <p id="campo-nombre-error" className={estilos.textoError}>
              {errorNombre}
            </p>
          )}
        </div>
      </section>

      <div className={estilos.encabezadoHabilidades}>
        <h2 className={estilos.tituloSeccion}>Habilidades</h2>
        <p className={estilos.ayuda}>
          Valores de {VALOR_MINIMO_HABILIDAD} a {VALOR_MAXIMO_HABILIDAD}. La
          puntuación y la posición sugerida las calcula el sistema al guardar.
        </p>
      </div>

      <div className={estilos.categorias}>
        {CATEGORIAS_HABILIDADES.map((categoria) => (
          <fieldset key={categoria.id} className={estilos.categoria}>
            <legend className={estilos.leyenda}>
              <span className={estilos[`cat_${categoria.id}`]} aria-hidden="true" />
              {categoria.titulo}
              <span className={estilos.conteo}>
                {categoria.habilidades.length}
              </span>
            </legend>
            {categoria.habilidades.map((habilidad) => (
              <ControlHabilidad
                key={habilidad}
                id={`habilidad-${habilidad}`}
                etiqueta={ETIQUETAS_HABILIDADES[habilidad]}
                valor={textos[habilidad]}
                error={errores[habilidad]}
                deshabilitado={enviando}
                alCambiar={(texto) => cambiarHabilidad(habilidad, texto)}
              />
            ))}
          </fieldset>
        ))}
      </div>

      <div className={estilos.barraAcciones}>
        <div className={`contenedor ${estilos.barraInterior}`}>
          {cantidadErrores > 0 && (
            <p className={estilos.resumenErrores} role="status">
              <IconoAlerta />
              Revisa {cantidadErrores}{" "}
              {cantidadErrores === 1 ? "campo" : "campos"}
            </p>
          )}
          <div className={estilos.botones}>
            <button
              type="button"
              className="boton boton--secundario"
              onClick={alCancelar}
              disabled={enviando}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="boton boton--primario"
              disabled={enviando}
            >
              {enviando ? (
                <>
                  <Spinner />
                  {textoEnviando}
                </>
              ) : (
                textoEnviar
              )}
            </button>
          </div>
        </div>
      </div>
    </form>
  );
}
