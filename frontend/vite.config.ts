import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// En desarrollo, las peticiones a /api se reenvían a FastAPI. Así el
// navegador nunca hace peticiones cross-origin, lo que permite abrir la
// app desde otro dispositivo de la red (p. ej. un móvil) sin problemas
// de CORS y sin modificar el backend.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, ".", "");
  const destinoApi = env.VITE_API_PROXY_TARGET || "http://localhost:8000";

  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: {
        "/api": {
          target: destinoApi,
          changeOrigin: true,
          rewrite: (ruta) => ruta.replace(/^\/api/, ""),
        },
      },
    },
  };
});
