"use client";

import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import {
  formatMessage,
  isLocale,
  Locale,
  TranslationKey,
  translations,
} from "@/i18n";

type I18nContextValue = {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: TranslationKey, vars?: Record<string, string | number>) => string;
};

const I18nContext = createContext<I18nContextValue | undefined>(undefined);

const DEFAULT_LOCALE: Locale = "ja";

const getInitialLocale = () => {
  if (typeof window === "undefined") {
    return DEFAULT_LOCALE;
  }

  const params = new URLSearchParams(window.location.search);
  const queryLocale = params.get("lang");
  if (isLocale(queryLocale)) {
    return queryLocale;
  }

  const storedLocale = window.localStorage.getItem("locale");
  if (isLocale(storedLocale)) {
    return storedLocale;
  }

  const browserLocale = window.navigator.language.toLowerCase();
  if (browserLocale.startsWith("ja")) return "ja";
  if (browserLocale.startsWith("ko")) return "ko";
  return "en";
};

export const I18nProvider = ({ children, initialLocale = DEFAULT_LOCALE }: { children: React.ReactNode; initialLocale?: Locale }) => {
  const [locale, setLocaleState] = useState<Locale>(initialLocale);

  useEffect(() => {
    setLocaleState(getInitialLocale());
  }, []);

  useEffect(() => {
    if (typeof window !== "undefined") {
      window.localStorage.setItem("locale", locale);
      document.documentElement.lang = locale;
      document.cookie = `udb-locale=${locale}; Path=/; Max-Age=31536000; SameSite=Lax${window.location.protocol === "https:" ? "; Secure" : ""}`;
      document.title = translations[locale]["meta.title"];
      const description = document.querySelector<HTMLMetaElement>('meta[name="description"]');
      if (description) description.content = translations[locale]["meta.description"];
      const manifest = document.querySelector<HTMLLinkElement>('link[rel="manifest"]');
      if (manifest) manifest.href = `/api/manifest?lang=${locale}`;
    }
  }, [locale]);

  const setLocale = useCallback((nextLocale: Locale) => {
    setLocaleState(nextLocale);
  }, []);

  const t = useCallback(
    (key: TranslationKey, vars?: Record<string, string | number>) => {
      const dictionary = translations[locale] ?? translations[DEFAULT_LOCALE];
      const template = dictionary[key] ?? translations[DEFAULT_LOCALE][key] ?? key;
      return formatMessage(template, vars);
    },
    [locale]
  );

  const value = useMemo(
    () => ({
      locale,
      setLocale,
      t,
    }),
    [locale, setLocale, t]
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
};

export const useI18n = () => {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error("useI18n must be used within an I18nProvider");
  }
  return context;
};
