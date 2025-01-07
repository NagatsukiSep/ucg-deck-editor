import  {DeckCards}  from "@/types/deckCard";
import { calculateChecksum } from "@/utils/calculateCheckSum";
import { BASE64_CHARS } from "@/utils/base64Chars";

export function decodeDeck(encoded: string): DeckCards {
    const checksumLength = 1; // チェックサムの長さ（例: calculateChecksum で生成）
    const body = encoded.slice(0, -checksumLength); // チェックサムを除いた部分
    const checksum = encoded.slice(-checksumLength); // チェックサム部分
  
    // チェックサムの検証
    if (calculateChecksum(body) !== checksum) {
      throw new Error("Invalid checksum. The encoded deck data is corrupted.");
    }
  
    const deck: DeckCards = {};
    for (let i = 0; i < body.length; i += 3) {
      const encodedChunk = body.slice(i, i + 3);
      if (encodedChunk.length !== 3) {
        throw new Error("Invalid encoded data length.");
      }
  
      const decade =
        BASE64_CHARS.indexOf(encodedChunk[0]) * 4096 +
        BASE64_CHARS.indexOf(encodedChunk[1]) * 64 +
        BASE64_CHARS.indexOf(encodedChunk[2]);
  
      const count = Math.floor(decade / 65536) === 0?4:Math.floor(decade / 65536); // カウント部分を取得
      const cardId = (decade % 65536).toString(); // カードID部分を取得
  
      if (!deck[cardId]) {
        deck[cardId] = 0;
      }
      deck[cardId] += count;
    }
  
    return deck;
  } 
  

// // 使用例
// try {
//     const encodedStr = "00z004yB+";
//     const decoded = decodeWithChecksum(encodedStr);
//     console.log(`Decoded: ${decoded}`);
// } catch (error) {
//     console.error(error instanceof Error ? error.message : error);
// }
