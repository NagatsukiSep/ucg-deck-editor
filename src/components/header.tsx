"use client";
import Link from "next/link";
import Image from "next/image";
import { useI18n } from "@/i18n/I18nProvider";

const localeLabelKey = {
  ja: "locale.ja",
  en: "locale.en",
  ko: "locale.ko",
} as const;

export default function Header() {
  const { t, locale, setLocale } = useI18n();

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
        <nav className="flex flex-1 items-center gap-4 ml-12">
          <ul className="flex gap-6">
            <li>
              <Link href="/" className="text-black hover:underline">
                {t("nav.top")}
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
      </div>
    </header>
  );
}
