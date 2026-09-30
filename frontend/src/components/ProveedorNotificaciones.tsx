import { useCallback, useMemo, useRef, useState, type ReactNode } from "react";

import {
  ContextoNotificaciones,
  type Notificacion,
} from "../hooks/useNotificaciones";
import { IconoAlerta, IconoCerrar, IconoCheck } from "./Iconos";
import estilos from "./ProveedorNotificaciones.module.css";

const DURACION_MS = 5000;

export function ProveedorNotificaciones({ children }: { children: ReactNode }) {
  const [notificaciones, setNotificaciones] = useState<Notificacion[]>([]);
  const siguienteId = useRef(1);

  const descartar = useCallback((id: number) => {
    setNotificaciones((actuales) => actuales.filter((n) => n.id !== id));
  }, []);

  const notificar = useCallback(
    (notificacion: Omit<Notificacion, "id">) => {
      const id = siguienteId.current++;
      setNotificaciones((actuales) => [...actuales, { ...notificacion, id }]);
      window.setTimeout(() => descartar(id), DURACION_MS);
    },
    [descartar],
  );

  const valor = useMemo(() => ({ notificar }), [notificar]);

  return (
    <ContextoNotificaciones.Provider value={valor}>
      {children}
      <div className={estilos.region} aria-live="polite">
        {notificaciones.map((n) => (
          <div
            key={n.id}
            className={`${estilos.notificacion} ${estilos[n.tipo]}`}
            role={n.tipo === "error" ? "alert" : "status"}
          >
            <span className={estilos.icono}>
              {n.tipo === "exito" ? <IconoCheck /> : <IconoAlerta />}
            </span>
            <div className={estilos.texto}>
              <p className={estilos.titulo}>{n.titulo}</p>
              {n.detalle && <p className={estilos.detalle}>{n.detalle}</p>}
            </div>
            <button
              type="button"
              className={estilos.cerrar}
              onClick={() => descartar(n.id)}
              aria-label="Cerrar notificación"
            >
              <IconoCerrar />
            </button>
          </div>
        ))}
      </div>
    </ContextoNotificaciones.Provider>
  );
}
