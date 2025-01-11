"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CardDetail } from "@/types/deckCard";
import { get } from "@/utils/request";
import { useEffect, useState, use, useRef } from "react";

export default function Home(props: { params: Promise<{ deckCode: string }> }) {
  const params = use(props.params);
  const { deckCode } = params;
  const didRun = useRef(false);
  const [is404, setIs404] = useState(false);
  const [deckCards, setDeckCards] = useState<CardDetail[]>([]);
  const [loadingDetails, setLoadingDetails] = useState(false);

  async function getDeckData() {
    setLoadingDetails(true);
    const data = await get<{ deck_cards: string }>(
      `/deck?deck_code=${deckCode}`
    );
    if (data.length === 0) {
      setIs404(true);
      return;
    }

    try {
      setDeckCards(JSON.parse(data[0].deck_cards));
    } catch (error) {
      console.error("Failed to parse JSON:", error);
    }
    setLoadingDetails(false);
    // await parseDeckCards(data[0].deck_cards);
  }

  useEffect(() => {
    if (didRun.current) return; // 2回目以降はスキップ
    didRun.current = true;
    getDeckData();
  }, [deckCode]);

  const handleGenerateCollage = async () => {
    try {
      const response = await fetch("/api/generate-image", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          images: deckCards.map((card) => ({ imagePath: card.image_url })),
          count: deckCards.map((card) => card.count),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate collage");
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      window.open(url, "_blank");
    } catch (error) {
      console.error(error);
      alert("Failed to generate collage");
    }
  };

  return (
    <div className="container mx-auto p-4 ">
      <h1 className="text-2xl font-bold mb-4">デッキ表示</h1>
      {is404 && (
        <div>
          <p>デッキが見つかりませんでした。</p>
          <Button
            onClick={() => {
              window.location.href = "/";
            }}
            className="mt-4"
          >
            トップに戻る
          </Button>
        </div>
      )}

      {deckCards.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>
              <h2 className="text-xl font-bold">
                デッキコード{deckCode}のデッキ情報
              </h2>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Button
              onClick={() => {
                navigator.clipboard.writeText(deckCode);
              }}
              className="m-2"
            >
              デッキコードをコピー
            </Button>
            <Button
              onClick={() => {
                handleGenerateCollage();
              }}
              className="m-2"
            >
              デッキ画像を表示
            </Button>
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
                    <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 bg-[#171717] text-center rounded-sm px-2 py-1 mb-2 w-8">
                      <div className="text-white">{card.count}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
