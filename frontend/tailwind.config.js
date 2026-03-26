/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#10212b",
        mist: "#eef3ef",
        clay: "#d97757",
        pine: "#24493f",
        sun: "#f7c65f",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Plus Jakarta Sans'", "sans-serif"],
      },
      boxShadow: {
        panel: "0 18px 45px rgba(16, 33, 43, 0.12)",
      },
      backgroundImage: {
        "hero-grid":
          "radial-gradient(circle at 20% 20%, rgba(247, 198, 95, 0.35), transparent 30%), radial-gradient(circle at 80% 10%, rgba(217, 119, 87, 0.22), transparent 32%), linear-gradient(135deg, rgba(36, 73, 63, 0.08), rgba(255, 255, 255, 0))",
      },
    },
  },
  plugins: [],
};
