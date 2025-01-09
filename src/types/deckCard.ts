export type DeckCards = {
  [key: string]: number;
}

export type CardDetail = {
  id: string;
  detail_name: string;
  image_url: string;
  count?: number;
};