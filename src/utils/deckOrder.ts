import { CardDetail } from "@/types/deckCard";
import { DeckAnalysis } from "@/types/deckCard";

export const autoSortDeck = (
  deckCards: CardDetail[],
  deckAnalysis: DeckAnalysis
): CardDetail[] => {
  const levelOrder = {
    ultra_hero: ["3", "2", "1"],
    kaiju: ["7", "6", "5", "4"],
    ultra_mech: ["3", "2", "1"],
  };

  const characterFeatureMap = new Map<string, string>();
  deckCards.forEach((card) => {
    if (card.character_name && card.feature_value) {
      characterFeatureMap.set(card.character_name, card.feature_value);
    }
  });
  if (deckAnalysis.scene !== undefined) {
    characterFeatureMap.set("scene", "scene");
  }

  const getGenreRankByFeature = (feature?: string): number => {
    switch (feature) {
      case "ultra_hero":
        return 0;
      case "ultra_mech":
        return 1;
      case "kaiju":
        return 2;
      case "boost":
        return 3;
      case "scene":
        return 4;
      default:
        return 5;
    }
  };

  const getCharTotal = (name: string) => {
    const value = deckAnalysis[name];
    if (!value) return 0; // undefined/null 安全対策
    if (typeof value === "number") return value; // scene
    return Object.values(value).reduce((sum, n) => sum + n, 0);
  };

  const isUltraHero = (name: string) =>
    typeof deckAnalysis[name] !== "number" &&
    Object.keys(deckAnalysis[name]!).some((level) => ["1", "2", "3"].includes(level));

  const isKaiju = (name: string) =>
    typeof deckAnalysis[name] !== "number" &&
    Object.keys(deckAnalysis[name]!).some((level) => ["4", "5", "6", "7"].includes(level));

  const isUltraMecha = (name: string) =>
    typeof deckAnalysis[name] !== "number" &&
    characterFeatureMap.get(name) === "ultra_mech";


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
        const feature = characterFeatureMap.get(name);
        if (feature) {
          return getGenreRankByFeature(feature);
        }
        return isUltraHero(name) ? 0 : isUltraMecha(name) ? 1 : isKaiju(name) ? 2 : 3;
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

  const groups = new Map<string, CardDetail[]>();
  for (const card of deckCards) {
    const key = card.group_key || card.id;
    const group = groups.get(key) || [];
    group.push(card);
    groups.set(key, group);
  }

  const sorted = [...groups.values()].sort((groupA, groupB) => {
    const a = groupA[0];
    const b = groupB[0];
    const charA = a.character_name ?? "";
    const charB = b.character_name ?? "";

    // sceneは最後にまとめて表示
    if (a.feature_value === "scene" && b.feature_value !== "scene") return 1; // aがシーン
    if (b.feature_value === "scene" && a.feature_value !== "scene") return -1; // bがシーン

    // ブーストはキャラクターカードの後、シーンの前にまとめる。
    if (a.feature_value === "boost" && b.feature_value !== "boost") return 1;
    if (b.feature_value === "boost" && a.feature_value !== "boost") return -1;

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

    // 同じカードの全絵柄を合算して、グループ単位の採用枚数順にする。
    const countA = groupA.reduce((sum, card) => sum + (card.count ?? 1), 0);
    const countB = groupB.reduce((sum, card) => sum + (card.count ?? 1), 0);
    return countB - countA;
  });

  // 同数では入力順を維持し、絵柄のID・採用枚数は変更しない。
  return sorted.flatMap(group => [...group].sort((a, b) => (b.count ?? 1) - (a.count ?? 1)));
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
