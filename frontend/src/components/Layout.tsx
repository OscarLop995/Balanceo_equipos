import { Link, NavLink, Outlet } from "react-router-dom";

import { IconoBalon, IconoCancha, IconoJugadores } from "./Iconos";
import estilos from "./Layout.module.css";

function claseEnlace({ isActive }: { isActive: boolean }) {
  return `${estilos.enlace} ${isActive ? estilos.activo : ""}`;
}

export function Layout() {
  return (
    <div className={estilos.app}>
      <header className={estilos.barra}>
        <div className={`contenedor ${estilos.barraInterior}`}>
          <Link to="/" className={estilos.marca}>
            <span className={estilos.logo}>
              <IconoBalon />
            </span>
            <span className={estilos.nombreMarca}>
              Balanceador <span>de Equipos</span>
            </span>
          </Link>

          <nav aria-label="Principal" className={estilos.nav}>
            <NavLink to="/" end className={claseEnlace} aria-label="Jugadores">
              <IconoJugadores />
              <span>Jugadores</span>
            </NavLink>
            <NavLink
              to="/partidos/nuevo"
              className={claseEnlace}
              aria-label="Nuevo partido"
            >
              <IconoCancha />
              <span>Nuevo partido</span>
            </NavLink>
          </nav>
        </div>
      </header>

      <main className={estilos.principal}>
        <Outlet />
      </main>
    </div>
  );
}
