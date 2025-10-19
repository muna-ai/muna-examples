/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "**.muna.ai" },
    ],
  },
};

export default nextConfig;
