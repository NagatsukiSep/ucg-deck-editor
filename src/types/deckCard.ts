export type DeckCards = {
  [key: string]: number;
}

export type CardDetail = {
  id: string;
  base_card_key?: string;
  branch?: string | null;
  number?: string;
  rarity_description?: string;
  detail_name: string;
  image_url: string;
  thumbnail_image_url?: string;
  level?: number;
  character_name?: string;
  feature_value?: string;
  count?: number;
  type_value?: "ultra_hero" | "kaiju" | "ultra_mech" | "scene";
};

export type DeckAnalysis = {
  [name: string]: {
    [level: string]: number;
  } | number;
};

export type StoredDeckCard = {
  id: string;
  count: number;
  base_card_key?: string;
  feature_value?: string;
  character_name?: string;
};
