export type DeckCards = {
  [key: string]: number;
}

export type CardDetail = {
  id: string;
  detail_name: string;
  image_url: string;
  level?: number;
  character_name?: string;
  feature_value?: string;
  count?: number;
  type_value?: "ultra_hero" | "kaiju" | "scene";
};

export type DeckAnalysis = {
  [name: string]: {
    [level: string]: number;
  } | number;
};