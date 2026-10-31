export type DeckCards = {
  [key: string]: number;
}

export type CardDetail = {
  id: string;
  artworks?: CardDetail[];
  artwork_count?: number;
  rarity?: string;
  management_number?: string;
  code?: string;
  group_key?: string;
  limit_count?: number;
  card_data_version?: number;
  effect?: string;
  detail_name: string;
  image_url: string;
  thumbnail_image_url?: string;
  level?: number;
  character_name?: string;
  feature_value?: string;
  count?: number;
  type_value?: string;
};

export type DeckAnalysis = {
  [name: string]: {
    [level: string]: number;
  } | number;
};
