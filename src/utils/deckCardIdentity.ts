import { CardDetail, StoredDeckCard } from "@/types/deckCard";

const BASE_CARD_NUMBER_PATTERN = /[A-Z]+\d{2}-[A-Z]?\d{3}|PR-\d{3}/g;

export const extractBaseCardKey = (number?: string | null) => {
  const rawNumber = number?.trim();
  if (!rawNumber) {
    return "";
  }

  const matches = rawNumber.match(BASE_CARD_NUMBER_PATTERN);
  if (matches && matches.length > 0) {
    return matches[matches.length - 1];
  }

  return rawNumber;
};

export const resolveBaseCardKey = (card: {
  id?: string;
  base_card_key?: string;
  number?: string | null;
}) => {
  const explicitKey = card.base_card_key?.trim();
  if (explicitKey) {
    return explicitKey;
  }

  const derivedKey = extractBaseCardKey(card.number);
  if (derivedKey) {
    return derivedKey;
  }

  return card.id ?? "";
};

export const withBaseCardKey = <T extends CardDetail>(card: T): T => ({
  ...card,
  base_card_key: resolveBaseCardKey(card),
});

export const serializeDeckCards = (cards: CardDetail[]): StoredDeckCard[] =>
  cards.map((card) => ({
    id: card.id,
    count: card.count ?? 0,
    base_card_key: resolveBaseCardKey(card),
    feature_value: card.feature_value,
    character_name: card.character_name,
  }));

export const parseStoredDeckCards = (raw: string): StoredDeckCard[] => {
  const parsed = JSON.parse(raw) as unknown;
  if (!Array.isArray(parsed)) {
    return [];
  }

  return parsed.flatMap((item) => {
    if (!item || typeof item !== "object") {
      return [];
    }

    const candidate = item as Record<string, unknown>;
    const id = candidate.id;
    const count = candidate.count;

    if (typeof id !== "string" || typeof count !== "number") {
      return [];
    }

    return [
      {
        id,
        count,
        base_card_key:
          typeof candidate.base_card_key === "string"
            ? candidate.base_card_key
            : undefined,
        feature_value:
          typeof candidate.feature_value === "string"
            ? candidate.feature_value
            : undefined,
        character_name:
          typeof candidate.character_name === "string"
            ? candidate.character_name
            : undefined,
      },
    ];
  });
};
