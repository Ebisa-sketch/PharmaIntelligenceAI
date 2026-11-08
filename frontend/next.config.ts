import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  images: {
    remotePatterns: [],
  },
  experimental: {
    typedRoutes: true,
  },
};

export default nextConfig;
