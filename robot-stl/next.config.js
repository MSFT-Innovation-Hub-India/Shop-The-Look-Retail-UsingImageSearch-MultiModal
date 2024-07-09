module.exports = {
    reactStrictMode: false,
    async rewrites() {
      return [
        {
          source: '/api/:path*',
          destination: 'http://127.0.0.1:5328/api/:path*', // Proxy to Backend
        },
      ]
    },
    images: {
        remotePatterns: [
          {
            protocol: 'http',
            hostname: 'assets.myntassets.com',
          },
        ],
      },
  }