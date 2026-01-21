"use client";
import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import { useI18n } from "@/i18n/I18nProvider";

const localeLabelKey = {
  ja: "locale.ja",
  en: "locale.en",
  ko: "locale.ko",
} as const;

export default function Header() {
  const { t, locale, setLocale } = useI18n();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="border-b px-4 py-3">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        {/* ロゴ部分 */}
        <Link href="/">
          <Image
            src="/logo.png"
            alt={t("header.logoAlt")}
            width={154}
            height={77}
            priority
            className="cursor-pointer h-9 w-auto md:h-[77px]"
          />
        </Link>

        {/* ナビゲーション部分 */}
        <nav className="hidden flex-1 items-center gap-4 ml-12 md:flex">
          <ul className="flex gap-6">
            <li>
              <Link href="/" className="text-black hover:underline">
                {t("nav.top")}
              </Link>
            </li>
            <li>
              <Link href="/new" className="text-black hover:underline">
                {t("nav.newDeck")}
              </Link>
            </li>
            <li>
              <Link href="/mydeck" className="text-black hover:underline">
                {t("nav.myDecks")}
              </Link>
            </li>
          </ul>
          <div className="ml-auto flex items-center gap-2 text-xs font-medium text-gray-700">
            <span>{t("header.languageLabel")}:</span>
            <select
              value={locale}
              onChange={(event) =>
                setLocale(event.target.value as "ja" | "en" | "ko")
              }
              className="rounded-md border border-gray-300 bg-white px-2 py-1 text-xs font-medium text-gray-700"
              aria-label={`${t("header.languageLabel")}: ${t(
                localeLabelKey[locale]
              )}`}
            >
              <option value="ja">{t("locale.ja")}</option>
              <option value="en">{t("locale.en")}</option>
              <option value="ko">{t("locale.ko")}</option>
            </select>
          </div>
        </nav>
        <div className="md:hidden">
          <button
            type="button"
            className="rounded-md border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700"
            onClick={() => setIsMenuOpen((open) => !open)}
            aria-expanded={isMenuOpen}
            aria-controls="mobile-menu"
          >
            {t("header.menu")}
          </button>
        </div>
      </div>
      {isMenuOpen && (
        <div
          id="mobile-menu"
          className="md:hidden border-t border-gray-200 bg-white"
        >
          <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4">
            <Link
              href="/"
              className="text-sm font-medium text-gray-900"
              onClick={() => setIsMenuOpen(false)}
            >
              {t("nav.top")}
            </Link>
            <Link
              href="/new"
              className="text-sm font-medium text-gray-900"
              onClick={() => setIsMenuOpen(false)}
            >
              {t("nav.newDeck")}
            </Link>
            <Link
              href="/mydeck"
              className="text-sm font-medium text-gray-900"
              onClick={() => setIsMenuOpen(false)}
            >
              {t("nav.myDecks")}
            </Link>
            <div className="flex items-center gap-2 text-xs font-medium text-gray-700">
              <span>{t("header.languageLabel")}:</span>
              <select
                value={locale}
                onChange={(event) => {
                  setLocale(event.target.value as "ja" | "en" | "ko");
                  setIsMenuOpen(false);
                }}
                className="rounded-md border border-gray-300 bg-white px-2 py-1 text-xs font-medium text-gray-700"
                aria-label={`${t("header.languageLabel")}: ${t(
                  localeLabelKey[locale]
                )}`}
              >
                <option value="ja">{t("locale.ja")}</option>
                <option value="en">{t("locale.en")}</option>
                <option value="ko">{t("locale.ko")}</option>
              </select>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
