import en from "@/i18n/translations/en.json";
import ja from "@/i18n/translations/ja.json";

export const translations = {
  en,
  ja,
} as const;

export type Locale = keyof typeof translations;
export type TranslationKey = keyof typeof ja;

export const isLocale = (value?: string | null): value is Locale =>
  value === "ja" || value === "en";

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
