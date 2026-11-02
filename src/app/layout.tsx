import { requestLocale } from "@/server/locale";
import { translations } from "@/i18n";
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

export async function generateMetadata(): Promise<Metadata> {
  const locale = await requestLocale();
  return {
  title: translations[locale]["meta.title"],
  description: translations[locale]["meta.description"],
  applicationName: "Ultra Deck Builder",
  manifest: `/api/manifest?lang=${locale}`,
  icons: {
    icon: "/icon_origin.png",
    apple: "/icon_origin.png",
    shortcut: "/icon_origin.png",
  },
  appleWebApp: {
    capable: true,
    title: "Ultra Deck Builder",
    statusBarStyle: "default",
  },
};
}

export const viewport: Viewport = {
  themeColor: "#111827",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const locale = await requestLocale();
  return (
    <html lang={locale}>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <I18nProvider initialLocale={locale}>
          <Header />
          <AppProvider>{children}</AppProvider>
        </I18nProvider>
        <PwaRegister />
        <Analytics />
      </body>
    </html>
  );
}
