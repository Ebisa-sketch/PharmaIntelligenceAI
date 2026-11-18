/** @type {import('next').NextConfig} */
const nextConfig = {
  // 'standalone' output is set via NEXT_OUTPUT_MODE env var in Docker builds only.
  // On Windows, standalone fails due to symlink permission restrictions.
  ...(process.env.NEXT_OUTPUT_MODE === 'standalone' ? { output: 'standalone' } : {}),
  reactStrictMode: true,
  poweredByHeader: false,
  images: {
    remotePatterns: [],
  },
};

export default nextConfig;
