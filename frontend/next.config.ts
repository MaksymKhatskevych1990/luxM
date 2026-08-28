import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // Keep trailing slashes for Django APPEND_SLASH via /api/[...path] proxy.
  skipTrailingSlashRedirect: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
      {
        protocol: "http",
        hostname: "localhost",
      },
      {
        protocol: "http",
        hostname: "127.0.0.1",
      },
    ],
  },
};

export default nextConfig;
