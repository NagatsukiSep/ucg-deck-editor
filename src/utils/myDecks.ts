export type SavedDeck = {
  code: string;
  name: string;
  savedAt: string;
};

const STORAGE_KEY = "myDeckCodes";

const normalizeSavedDeck = (value: unknown): SavedDeck | null => {
  if (typeof value !== "object" || value === null) {
    return null;
  }

  const record = value as Partial<SavedDeck> & {
    code?: unknown;
    name?: unknown;
    savedAt?: unknown;
  };

  if (typeof record.code !== "string" || typeof record.savedAt !== "string") {
    return null;
  }

  const code = record.code.trim();
  if (!code) {
    return null;
  }

  const name =
    typeof record.name === "string" && record.name.trim().length > 0
      ? record.name.trim()
      : code;

  return {
    code,
    name,
    savedAt: record.savedAt,
  };
};

export const getSavedDecks = (): SavedDeck[] => {
  if (typeof window === "undefined") {
    return [];
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed
      .map((item) => normalizeSavedDeck(item))
      .filter((item): item is SavedDeck => item !== null);
  } catch (error) {
    console.error("Failed to read saved decks:", error);
    return [];
  }
};

const persistDecks = (decks: SavedDeck[]) => {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(decks));
};

export const saveDeckCode = (code: string, name: string) => {
  const normalized = code.trim();
  const normalizedName = name.trim();
  if (!normalized || !normalizedName) {
    return { saved: false, alreadySaved: false };
  }

  const decks = getSavedDecks();
  const alreadySaved = decks.some((deck) => deck.code === normalized);
  if (alreadySaved) {
    return { saved: false, alreadySaved: true };
  }

  const nextDecks: SavedDeck[] = [
    { code: normalized, name: normalizedName, savedAt: new Date().toISOString() },
    ...decks,
  ];
  persistDecks(nextDecks);
  return { saved: true, alreadySaved: false };
};

export const removeDeckCode = (code: string) => {
  const normalized = code.trim();
  if (!normalized) {
    return getSavedDecks();
  }
  const nextDecks = getSavedDecks().filter(
    (deck) => deck.code !== normalized
  );
  persistDecks(nextDecks);
  return nextDecks;
};
