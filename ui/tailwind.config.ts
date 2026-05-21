import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#050816",
        panels: "#0B1120",
        border: "rgba(255,255,255,0.08)",
        primary: {
          DEFAULT: "#00D1FF",
          accent: "#7B61FF",
        },
        gold: "#F4B942",
        success: "#00FFAE",
        warning: "#FFB020",
        critical: "#FF4D6D",
      },
      fontFamily: {
        inter: ["var(--font-inter)"],
        space: ["var(--font-space-grotesk)"],
      },
    },
  },
  plugins: [],
};
export default config;
