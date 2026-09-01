/** @type {import('next').NextConfig} */
const path = require('path');

const nextConfig = {
  experimental: { appDir: true },
  distDir: path.join('apps', 'frontend', '.next'),
};

module.exports = nextConfig;
