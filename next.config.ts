import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    domains: ['api.ultraman-cardgame.com', "ucg-deck-editor.innovatz.jp", "ud-builder.innovatz.jp"],
    unoptimized: true,
  },
};

export default nextConfig;
