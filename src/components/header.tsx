"use client";
import Link from "next/link";
import Image from "next/image";
import { useI18n } from "@/i18n/I18nProvider";

export default function Header() {
  const { t, locale, setLocale } = useI18n();
  const nextLocale = locale === "ja" ? "en" : "ja";

  return (
    <header className="border-b px-4 py-3">
      <div className="mx-auto flex max-w-7xl items-center justify-start">
        {/* ロゴ部分 */}
        <Link href="/">
          <Image
            src="/logo.png"
            alt={t("header.logoAlt")}
            width={154}
            height={77}
            priority
            className="cursor-pointer"
          />
        </Link>

        {/* ナビゲーション部分 */}
        <nav className="flex items-center gap-4 ml-12">
          <ul className="flex gap-6">
            <li>
              <Link href="/" className="text-black hover:underline">
                {t("nav.top")}
              </Link>
            </li>
          </ul>
          <button
            type="button"
            className="rounded-md border border-gray-300 px-2 py-1 text-xs font-medium text-gray-700 hover:bg-gray-100"
            onClick={() => setLocale(nextLocale)}
          >
            {nextLocale === "en"
              ? t("header.switchToEnglish")
              : t("header.switchToJapanese")}
          </button>
        </nav>
      </div>
    </header>
  );
}
