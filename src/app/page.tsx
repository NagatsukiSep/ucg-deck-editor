"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { CardDetail } from "@/types/deckCard";
import { get } from "@/utils/request";

export default function Home() {
  const [deckCode, setDeckCode] = useState("");
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = await get(`/deck?deck_code=${deckCode}`);
    await parseDeckCards(data[0].deck_cards);
  };

  return (
    <div className="container mx-auto p-4 ">
      <h1 className="text-2xl font-bold mb-4">デッキコード入力</h1>
      <p className="text-gray-600 mb-6">デッキコードを入力してください。</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="deckCode" className="text-sm font-medium">
            デッキコード
          </Label>
          <Input
            id="deckCode"
            placeholder="デッキコードを入力"
            value={deckCode}
            onChange={(e) => setDeckCode(e.target.value)}
            className="w-full"
          />
        </div>
        <Button type="submit" className="w-full">
          送信
        </Button>
      </form>
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
