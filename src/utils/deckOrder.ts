import { CardDetail } from "@/types/deckCard";
import { DeckAnalysis } from "@/types/deckCard";

export const autoSortDeck = (
  deckCards: CardDetail[],
  deckAnalysis: DeckAnalysis
): CardDetail[] => {
  const levelOrder = {
    ultra_hero: ["3", "2", "1"],
    kaiju: ["7", "6", "5", "4"],
    ultra_mecha: ["3", "2", "1"],
  };

  const nameFeatureMap = new Map<string, string>();
  deckCards.forEach((card) => {
    if (!card.character_name || !card.feature_value) return;
    if (card.feature_value === "scene") return;
    if (!nameFeatureMap.has(card.character_name)) {
      nameFeatureMap.set(card.character_name, card.feature_value);
    }
  });

  const getCharTotal = (name: string) => {
    const value = deckAnalysis[name];
    if (!value) return 0; // undefined/null 安全対策
    if (typeof value === "number") return value; // scene
    return Object.values(value).reduce((sum, n) => sum + n, 0);
  };

  const getFeatureByName = (name: string) => nameFeatureMap.get(name);

  const getHighLevelCount = (name: string): number => {
    const value = deckAnalysis[name];
    if (typeof value === "number") return 0;
    return (value["3"] ?? 0) + (value["7"] ?? 0); // 高レベル: Ultra=3, Kaiju=7
  };

  const charaOrder = Object.keys(deckAnalysis)
    .filter((name) => name !== "") // 念のため空キー回避
    .sort((a, b) => {
      // ①ジャンル順
      const getGenreRank = (name: string): number => {
        if (name === "シーン") return 3;
        switch (getFeatureByName(name)) {
          case "ultra_hero":
            return 0;
          case "kaiju":
            return 1;
          case "ultra_mecha":
            return 2;
          default:
            return 3;
        }
      };

      const genreDiff = getGenreRank(a) - getGenreRank(b);
      if (genreDiff !== 0) return genreDiff;

      // ②総合枚数順
      const totalDiff = getCharTotal(b) - getCharTotal(a);
      if (totalDiff !== 0) return totalDiff;

      // ③高レベル優先
      const highLevelDiff = getHighLevelCount(b) - getHighLevelCount(a);
      if (highLevelDiff !== 0) return highLevelDiff;

      // ④五十音順（ローマ字での比較でもOK）
      return a.localeCompare(b, "ja");
    });

  const sorted = [...deckCards].sort((a, b) => {
    const charA = a.character_name ?? "";
    const charB = b.character_name ?? "";

    // sceneは最後にまとめて表示
    if (a.feature_value === "scene" && b.feature_value !== "scene") return 1; // aがシーン
    if (b.feature_value === "scene" && a.feature_value !== "scene") return -1; // bがシーン

    // キャラ名の順序（charaOrderに従う）
    const indexA = charaOrder.indexOf(charA);
    const indexB = charaOrder.indexOf(charB);
    if (indexA !== indexB) return indexA - indexB;

    // 同じキャラ内でレベル順
    const type = a.feature_value ?? "";

    const levelA = a.level?.toString() ?? "";
    const levelB = b.level?.toString() ?? "";

    const levels = levelOrder[type as keyof typeof levelOrder] ?? [];

    const levelIndexA = levels.indexOf(levelA);
    const levelIndexB = levels.indexOf(levelB);
    if (levelIndexA !== levelIndexB) return levelIndexA - levelIndexB;

    // レベルも同じなら、採用枚数順（降順）で
    const countA = a.count ?? 1;
    const countB = b.count ?? 1;
    return countB - countA;
  });

  return sorted;
};


export const changeIndex = (id: string, order: "up" | "down", deckCards: CardDetail[]) => {
  const index = deckCards.findIndex((card) => card.id === id);
  const newDeckCards = [...deckCards];
  if (index === -1) {
    return newDeckCards; // IDが見つからない場合はそのまま返す
  }
  if (order === "up") {
    if (index === 0) {
      return newDeckCards; // 先頭は移動できない
    }
    newDeckCards[index] = deckCards[index - 1];
    newDeckCards[index - 1] = deckCards[index];
  } else {
    if (index === deckCards.length - 1) {
      return newDeckCards; // 最後尾は移動できない
    }
    newDeckCards[index] = deckCards[index + 1];
    newDeckCards[index + 1] = deckCards[index];
  }
  return newDeckCards;
};

export const isEdge = (id: string, order: "up" | "down", deckCards: CardDetail[]) => {
  const index = deckCards.findIndex((card) => card.id === id);
  if (index === -1) {
    return false;
  }
  if (order === "up") {
    if (index === 0) {
      return true;
    }
  } else {
    if (index === deckCards.length - 1) {
      return true;
    }
  }
  return false;
};
