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
      ],
    },
  };

export default nextConfig;
