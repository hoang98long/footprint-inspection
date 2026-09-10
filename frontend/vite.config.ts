import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Local Vite runs outside Docker, whereas Compose resolves the backend service
// by its Docker DNS name. Compose supplies VITE_API_PROXY_TARGET below.
const apiProxyTarget = process.env.VITE_API_PROXY_TARGET ?? "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    proxy: {
      "/api": apiProxyTarget,
      "/health": apiProxyTarget,
    },
  },
});
