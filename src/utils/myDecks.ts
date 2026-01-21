export type SavedDeck = {
  code: string;
  savedAt: string;
};

const STORAGE_KEY = "myDeckCodes";

const isSavedDeck = (value: unknown): value is SavedDeck => {
  return (
    typeof value === "object" &&
    value !== null &&
    "code" in value &&
    "savedAt" in value &&
    typeof (value as SavedDeck).code === "string" &&
    typeof (value as SavedDeck).savedAt === "string"
  );
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
    return parsed.filter(isSavedDeck);
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

export const saveDeckCode = (code: string) => {
  const normalized = code.trim();
  if (!normalized) {
    return { saved: false, alreadySaved: false };
  }

  const decks = getSavedDecks();
  const alreadySaved = decks.some((deck) => deck.code === normalized);
  if (alreadySaved) {
    return { saved: false, alreadySaved: true };
  }

  const nextDecks: SavedDeck[] = [
    { code: normalized, savedAt: new Date().toISOString() },
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
