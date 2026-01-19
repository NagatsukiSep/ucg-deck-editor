import en from "@/i18n/translations/en.json";
import ja from "@/i18n/translations/ja.json";
import ko from "@/i18n/translations/ko.json";

export const translations = {
  en,
  ja,
  ko,
} as const;

export type Locale = keyof typeof translations;
export type TranslationKey = keyof typeof ja;

export const isLocale = (value?: string | null): value is Locale =>
  value === "ja" || value === "en" || value === "ko";

export const formatMessage = (
  template: string,
  variables?: Record<string, string | number>
) => {
  if (!variables) return template;
  return template.replace(/\{(\w+)\}/g, (match, key) => {
    if (Object.prototype.hasOwnProperty.call(variables, key)) {
      return String(variables[key]);
    }
    return match;
  });
};
