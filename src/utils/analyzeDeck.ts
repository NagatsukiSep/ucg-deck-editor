import { CardDetail, DeckAnalysis } from "@/types/deckCard";

export const analyzeDeck = (cards: CardDetail[]): DeckAnalysis => {
  const result: DeckAnalysis = {};

  for (const card of cards) {
    switch (card.feature_value) {
      case "ultra_hero": {
        const name = card.character_name ?? "不明ヒーロー";
        const rawLevel = card.level?.toString() ?? "不明";
        const level = rawLevel === "4" ? "4_hero" : rawLevel;

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

      case "ultra_mech": {
        const name = card.character_name ?? "不明メカ";
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

  const entries = Object.entries(result);
  entries.sort((a, b) => {
    const isAScene = a[0] === "シーン";
    const isBScene = b[0] === "シーン";
    if (isAScene && !isBScene) return 1;
    if (!isAScene && isBScene) return -1;

    const totalA =
      typeof a[1] === "number"
        ? a[1]
        : Object.values(a[1]).reduce((sum, n) => sum + n, 0);
    const totalB =
      typeof b[1] === "number"
        ? b[1]
        : Object.values(b[1]).reduce((sum, n) => sum + n, 0);
    return totalB - totalA;
  });

  const orderedResult: DeckAnalysis = {};
  for (const [name, value] of entries) {
    orderedResult[name] = value;
  }

  return orderedResult;
};
