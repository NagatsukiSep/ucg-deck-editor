import { CardDetail } from "@/types/deckCard";
import { resolveBaseCardKey, withBaseCardKey } from "@/utils/deckCardIdentity";

export const buildArtworkGroupKey = (card: {
  id?: string;
  base_card_key?: string;
  number?: string | null;
}) => resolveBaseCardKey(card);

export const sortArtworkCandidates = (
  cards: CardDetail[],
  currentCardId: string
) =>
  [...cards].sort((a, b) => {
    if (a.id === currentCardId) return -1;
    if (b.id === currentCardId) return 1;

    const aHasBranch = Boolean(a.branch?.trim());
    const bHasBranch = Boolean(b.branch?.trim());
    if (aHasBranch !== bHasBranch) {
      return aHasBranch ? 1 : -1;
    }

    return (a.number ?? "").localeCompare(b.number ?? "");
  });

export const fetchArtworkVariants = async (card: CardDetail) => {
  const baseCardKey = resolveBaseCardKey(card);
  if (!baseCardKey) {
    return [];
  }

  const response = await fetch(
    `/api/card-variants?base_card_key=${encodeURIComponent(baseCardKey)}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch artwork variants: ${response.status}`);
  }

  const rows = ((await response.json()) as CardDetail[]).map(withBaseCardKey);
  return sortArtworkCandidates(rows, card.id);
};
