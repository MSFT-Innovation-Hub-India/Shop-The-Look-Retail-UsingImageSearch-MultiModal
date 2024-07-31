/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'stlprojectstorage.blob.core.windows.net',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'http',  // or 'https' depending on the URL scheme
        hostname: 'assets.myntassets.com',
        port: '',
        pathname: '/**',
      },
    ],
  },
};

export default nextConfig;