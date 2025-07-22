import { CardDetail, DeckAnalysis } from "@/types/deckCard";

export const analyzeDeck = (cards: CardDetail[]): DeckAnalysis => {
  const result: DeckAnalysis = {};

  for (const card of cards) {
    switch (card.feature_value) {
      case "ultra_hero": {
        const name = card.character_name ?? "不明ヒーロー";
        const level = card.level?.toString() ?? "不明";

        if (!result[name]) {
          result[name] = {};
        }

        if (typeof result[name] === "number") {
          // number 型 → レベル付きに切り替える
          result[name] = { [level]: card.count ?? 0 };
        } else {
          const levelMap = result[name] as Record<string, number>;
          levelMap[level] = (levelMap[level] ?? 0) + (card.count ?? 0);
        }
        break;
      }

      case "kaiju": {
        const name = card.character_name ?? "不明怪獣";
        const level = card.level?.toString() ?? "不明";

        if (!result[name]) {
          result[name] = {};
        }

        if (typeof result[name] === "number") {
          result[name] = { [level]: card.count ?? 0 };
        } else {
          const levelMap = result[name] as Record<string, number>;
          levelMap[level] = (levelMap[level] ?? 0) + (card.count ?? 0);
        }
        break;
      }

      case "scene": {
        const name = "シーン";
        const prev = typeof result[name] === "number" ? result[name] : 0;
        result[name] = prev + (card.count ?? 0);
        break;
      }

      default:
        // 対応外はスキップ
        continue;
    }
  }

  return result;
};
