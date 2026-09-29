import type { NextConfig } from "next";

const BACKEND_ORIGIN = (
  process.env.INTERNAL_API_URL || "http://127.0.0.1:8000/api"
).replace(/\/api\/?$/, "");

const extraOrigins = (process.env.ALLOWED_DEV_ORIGINS || "")
  .split(",")
  .map((value) => value.trim())
  .filter(Boolean);

const nextConfig: NextConfig = {
  output: "standalone",
  // Keep trailing slashes for Django APPEND_SLASH via /api/[...path] proxy.
  skipTrailingSlashRedirect: true,
  async rewrites() {
    return [
      {
        source: "/media/:path*",
        destination: `${BACKEND_ORIGIN}/media/:path*`,
      },
    ];
  },
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "Access-Control-Allow-Origin", value: "*" },
          { key: "X-Robots-Tag", value: "noindex, nofollow, noarchive" },
        ],
      },
    ];
  },
  // Allow ngrok / LAN / other tunnels to load /_next assets in dev.
  allowedDevOrigins: [
    "*.ngrok-free.dev",
    "*.ngrok-free.app",
    "*.ngrok.io",
    "*.ngrok.app",
    "localhost",
    "127.0.0.1",
    ...extraOrigins,
  ],
  images: {
    unoptimized: process.env.NODE_ENV !== "production",
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
      {
        protocol: "http",
        hostname: "127.0.0.1",
        port: "8000",
        pathname: "/media/**",
      },
      {
        protocol: "http",
        hostname: "localhost",
        port: "8000",
        pathname: "/media/**",
      },
    ],
  },
};

export default nextConfig;
