import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AppProvider } from "@/context/AppContext";
import Header from "@/components/header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Ultra Deck Builder - ウルトラマンカードゲーム デッキビルダー",
  description:
    "Ultra Deck Builderは、ウルトラマンカードゲーム（UCG）専用の非公式デッキ作成ツールです。直感的なUIでデッキ構築・共有が簡単にできます。",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Header />
        <AppProvider>{children}</AppProvider>
      </body>
    </html>
  );
}
