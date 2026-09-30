import type { SVGProps } from "react";

type PropsIcono = SVGProps<SVGSVGElement>;

function Base({ children, ...props }: PropsIcono) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      {...props}
    >
      {children}
    </svg>
  );
}

export function IconoBalon(props: PropsIcono) {
  return (
    <Base {...props}>
      <circle cx="12" cy="12" r="9.5" />
      <path d="M12 7.5l4 2.9-1.5 4.7h-5L8 10.4z" fill="currentColor" stroke="none" />
      <path d="M12 7.5V2.5M16 10.4l4.6-1.5M14.5 15.1l2.8 3.9M9.5 15.1l-2.8 3.9M8 10.4L3.4 8.9" />
    </Base>
  );
}

export function IconoMas(props: PropsIcono) {
  return (
    <Base {...props}>
      <path d="M12 5v14M5 12h14" />
    </Base>
  );
}

export function IconoEditar(props: PropsIcono) {
  return (
    <Base {...props}>
      <path d="M4 20h4L19 9l-4-4L4 16z" />
      <path d="M13.5 6.5l4 4" />
    </Base>
  );
}

export function IconoVolver(props: PropsIcono) {
  return (
    <Base {...props}>
      <path d="M15 18l-6-6 6-6" />
    </Base>
  );
}

export function IconoCheck(props: PropsIcono) {
  return (
    <Base {...props}>
      <path d="M5 12.5l4.5 4.5L19 7.5" />
    </Base>
  );
}

export function IconoAlerta(props: PropsIcono) {
  return (
    <Base {...props}>
      <circle cx="12" cy="12" r="9.5" />
      <path d="M12 7.5v5.5M12 16.5v.01" />
    </Base>
  );
}

export function IconoRecargar(props: PropsIcono) {
  return (
    <Base {...props}>
      <path d="M20 11a8 8 0 1 0-2.3 5.7" />
      <path d="M20 4v7h-7" />
    </Base>
  );
}

export function IconoCancha(props: PropsIcono) {
  return (
    <Base {...props}>
      <rect x="2.5" y="5" width="19" height="14" rx="1.5" />
      <path d="M12 5v14" />
      <circle cx="12" cy="12" r="2.8" />
      <path d="M2.5 9.5h2.5v5H2.5M21.5 9.5H19v5h2.5" />
    </Base>
  );
}

export function IconoJugadores(props: PropsIcono) {
  return (
    <Base {...props}>
      <circle cx="9" cy="8" r="3.5" />
      <path d="M2.5 20c.6-3.6 3.3-5.5 6.5-5.5s5.9 1.9 6.5 5.5" />
      <path d="M16 4.8a3.5 3.5 0 0 1 0 6.4M18.5 14.8c1.6.8 2.7 2.5 3 5.2" />
    </Base>
  );
}

export function IconoCerrar(props: PropsIcono) {
  return (
    <Base {...props}>
      <path d="M6 6l12 12M18 6L6 18" />
    </Base>
  );
}

export function IconoServidor(props: PropsIcono) {
  return (
    <Base {...props}>
      <rect x="3.5" y="4" width="17" height="7" rx="1.5" />
      <rect x="3.5" y="13" width="17" height="7" rx="1.5" />
      <path d="M7.5 7.5h.01M7.5 16.5h.01" />
    </Base>
  );
}
