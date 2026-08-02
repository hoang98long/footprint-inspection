import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite build configuration; API proxying can be added after endpoint contracts exist.
export default defineConfig({
  plugins: [react()],
});
