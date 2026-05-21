import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  // Ensure images from potential enterprise asset servers are allowed if needed
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
};

export default nextConfig;
