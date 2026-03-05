import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";
import { AppProvider } from "@/context/AppContext";
import Header from "@/components/header";
import { I18nProvider } from "@/i18n/I18nProvider";
import PwaRegister from "@/components/pwa-register";

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
  applicationName: "Ultra Deck Builder",
  manifest: "/manifest.webmanifest",
  icons: {
    icon: "/favicon.ico",
    apple: "/favicon.ico",
  },
  appleWebApp: {
    capable: true,
    title: "Ultra Deck Builder",
    statusBarStyle: "default",
  },
};

export const viewport: Viewport = {
  themeColor: "#111827",
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
        <I18nProvider>
          <Header />
          <AppProvider>{children}</AppProvider>
        </I18nProvider>
        <PwaRegister />
        <Analytics />
      </body>
    </html>
  );
}
