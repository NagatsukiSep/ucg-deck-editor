"use client";

import { CardDetail } from "@/types/deckCard";
import { get } from "@/utils/request";
import { useEffect, useState } from "react";

export default function Home({ params }: { params: { deckCode: string } }) {
  const { deckCode } = params;
  const [deckCards, setDeckCards] = useState<CardDetail[]>([]);
  const [loadingDetails, setLoadingDetails] = useState(false);
  async function parseDeckCards(data: string) {
    setLoadingDetails(true);
    const parts = data.split("-");

    for (let i = 0; i < parts.length; i += 2) {
      const id = parts[i];
      const count = parseInt(parts[i + 1], 10);
      const data = await get(`/card?id=${id}`);
      const deckCard = {
        id: id,
        detail_name: data[0].detail_name,
        image_url: data[0].image_url,
        count,
      };
      setDeckCards((prev) => [...prev, deckCard]);
    }
    setLoadingDetails(false);
    return;
  }

  async function getDeckData() {
    const data = await get(`/deck?deck_code=${deckCode}`);
    await parseDeckCards(data[0].deck_cards);
  }

  useEffect(() => {
    getDeckData();
  }, [deckCode]);

  return (
    <div className="container mx-auto p-4 ">
      <div className="w-full h-0.5 bg-gray-200 my-6"></div>
      {deckCards.length > 0 && (
        <div className="mt-6">
          <h2 className="text-xl font-bold mb-4">{deckCode}のデッキ情報</h2>
          {loadingDetails ? (
            <p>カード情報を読み込んでいます...</p>
          ) : (
            <div className="flex flex-wrap mt-4">
              {deckCards.map((card) => (
                <div key={card.id} className="relative w-48">
                  <img
                    src={card.image_url}
                    alt={card.detail_name}
                    className="w-full h-auto"
                  />
                  <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 bg-white text-center rounded-sm px-2 py-1 mb-2">
                    {card.count}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
