import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    domains: ['api.ultraman-cardgame.com', "ucg-deck-editor.innovatz.jp"], // ホスト名を追加
  },
};

export default nextConfig;
