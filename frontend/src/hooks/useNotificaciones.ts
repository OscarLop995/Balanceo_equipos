import { createContext, useContext } from "react";

export type TipoNotificacion = "exito" | "error";

export interface Notificacion {
  id: number;
  tipo: TipoNotificacion;
  titulo: string;
  detalle?: string;
}

export interface ContextoNotificacionesValor {
  notificar: (notificacion: Omit<Notificacion, "id">) => void;
}

export const ContextoNotificaciones =
  createContext<ContextoNotificacionesValor | null>(null);

export function useNotificaciones(): ContextoNotificacionesValor {
  const contexto = useContext(ContextoNotificaciones);

  if (!contexto) {
    throw new Error(
      "useNotificaciones debe usarse dentro de <ProveedorNotificaciones>.",
    );
  }

  return contexto;
}
