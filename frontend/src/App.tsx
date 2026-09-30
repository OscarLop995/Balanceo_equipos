import { useEffect } from "react";
import {
  BrowserRouter,
  Route,
  Routes,
  useLocation,
} from "react-router-dom";

import { Layout } from "./components/Layout";
import { ProveedorNotificaciones } from "./components/ProveedorNotificaciones";
import { EditarJugadorPage } from "./pages/EditarJugadorPage";
import { InicioPage } from "./pages/InicioPage";
import { NoEncontradoPage } from "./pages/NoEncontradoPage";
import { NuevoPartidoPage } from "./pages/NuevoPartidoPage";
import { RegistrarJugadorPage } from "./pages/RegistrarJugadorPage";
import { ResultadoPage } from "./pages/ResultadoPage";

function DesplazarArribaAlNavegar() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}

export function App() {
  return (
    <BrowserRouter>
      <ProveedorNotificaciones>
        <DesplazarArribaAlNavegar />
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<InicioPage />} />
            <Route path="jugadores/nuevo" element={<RegistrarJugadorPage />} />
            <Route
              path="jugadores/:idJugador/editar"
              element={<EditarJugadorPage />}
            />
            <Route path="partidos/nuevo" element={<NuevoPartidoPage />} />
            <Route path="partidos/resultado" element={<ResultadoPage />} />
            <Route path="*" element={<NoEncontradoPage />} />
          </Route>
        </Routes>
      </ProveedorNotificaciones>
    </BrowserRouter>
  );
}
