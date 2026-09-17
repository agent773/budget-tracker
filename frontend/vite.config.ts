// Vite config.
//
// PSEUDOCODE:
//
// export default defineConfig({
//   plugins: [react()],
//   server: {
//     https: true,               // use the same self-signed cert as the backend during dev
//     proxy: {
//       "/api": "https://localhost:8000"   // forward API calls to FastAPI during `npm run dev`
//     }
//   },
//   build: { outDir: "dist" }    // this is what FastAPI serves statically in real usage
// })
