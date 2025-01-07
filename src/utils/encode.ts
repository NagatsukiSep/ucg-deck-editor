import  {DeckCards}  from "@/types/deckCard";
import { calculateChecksum } from "@/utils/calculateCheckSum";
import { BASE64_CHARS } from "@/utils/base64Chars";

export function encodeDeck(deck: DeckCards): string {
  let encoded = "";
  Object.entries(deck).forEach(([cardId, count]) => {
    // cardIdが適切かチェック
    const decade = count * 65536 + parseInt(cardId, 10);
    const encodedSingle =
      BASE64_CHARS[Math.floor(decade / 4096) % 64] +
      BASE64_CHARS[Math.floor(decade / 64) % 64] +
      BASE64_CHARS[decade % 64];
    encoded += encodedSingle;
  });
  const checksum = calculateChecksum(encoded);
  return encoded + checksum;
}
