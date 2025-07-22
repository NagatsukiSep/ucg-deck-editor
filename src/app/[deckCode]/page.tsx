"use client";

import DeckBarChart from "@/components/deckBarChart";
import { ImageWithSkeleton } from "@/components/image-with-skelton";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAppContext } from "@/context/AppContext";
import { CardDetail, DeckAnalysis } from "@/types/deckCard";
import { analyzeDeck } from "@/utils/analyzeDeck";
import { get } from "@/utils/request";
import { useRouter } from "next/navigation";
import { useEffect, useState, use, useRef, useCallback } from "react";

export default function Home(props: { params: Promise<{ deckCode: string }> }) {
  const params = use(props.params);
  const { deckCode } = params;
  const didRun = useRef(false);
  const [is404, setIs404] = useState(false);
  const [deckCards, setDeckCards] = useState<CardDetail[]>([]);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [deckAnalysis, setDeckAnalysis] = useState<DeckAnalysis>({});

  const getDeckData = useCallback(async () => {
    setLoadingDetails(true);
    try {
      const data = await get<{ deck_cards: string }>(
        `/deck?deck_code=${deckCode}`
      );
      if (data.length === 0) {
        setIs404(true);
        return;
      }

      // deck_cards をパースして ID一覧と count マップ作成
      const parsed: { id: string; count: number }[] = JSON.parse(
        data[0].deck_cards
      );
      const idToCount = new Map(parsed.map((card) => [card.id, card.count]));
      const cardIds = [...idToCount.keys()];
      const cardDetails = await get<CardDetail>(
        `/card_detail?ids=${cardIds.join(",")}`
      );
      const enrichedCards: CardDetail[] = cardDetails.map((card) => ({
        ...card,
        count: idToCount.get(card.id) ?? 0,
      }));

      // state に保存
      setDeckCards(enrichedCards);
      console.log("Deck cards:", enrichedCards);
      generateCollage(enrichedCards);
    } catch (error) {
      console.error("Failed to parse JSON:", error);
    }
    setLoadingDetails(false);
  }, [deckCode]);

  useEffect(() => {
    const analysis = analyzeDeck(deckCards);
    setDeckAnalysis(analysis);
    console.log("Deck analysis updated:", analysis);
  }, [deckCards]);

  useEffect(() => {
    if (didRun.current) return; // 2回目以降はスキップ
    didRun.current = true;
    getDeckData();
  }, [getDeckData]);

  const generateCollage = async (cards: CardDetail[]) => {
    setIsGeneratingImage(true);
    try {
      const response = await fetch("/api/generate-image", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          images: cards.map((card) => ({ imagePath: card.image_url })),
          count: cards.map((card) => card.count),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate collage");
      }

      const blob = await response.blob();
      setImageUrl(URL.createObjectURL(blob));
      setIsGeneratingImage(false);
    } catch (error) {
      console.error(error);
      alert("Failed to generate collage");
    }
  };

  const { setOriginalDeckCards } = useAppContext();
  const router = useRouter();

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
            <div className="flex flex-col md:flex-row items-center">
              <DeckBarChart analysis={deckAnalysis} />
              <div className="flex flex-col">
                <Button
                  onClick={() => {
                    navigator.clipboard.writeText(deckCode);
                    alert("デッキコードをコピーしました。");
                  }}
                  className="m-2"
                >
                  デッキコードをコピー
                </Button>
                <Button
                  onClick={() => {
                    navigator.clipboard.writeText(
                      `${window.location.origin}/${deckCode}`
                    );
                    alert("デッキコードをURL付きでコピーしました。");
                  }}
                  className="m-2"
                >
                  デッキコードをURL付きでコピー
                </Button>
              </div>
              <div className="flex flex-col">
                <Button
                  onClick={() => {
                    window.open(imageUrl, "_blank");
                  }}
                  className="m-2"
                  disabled={isGeneratingImage}
                >
                  {isGeneratingImage ? "読み込み中" : "デッキ画像を表示"}
                </Button>
                <Button
                  onClick={() => {
                    setOriginalDeckCards(deckCards);
                    router.push("/new");
                  }}
                  className="m-2"
                >
                  このデッキからデッキ作成
                </Button>
              </div>
            </div>
            {loadingDetails ? (
              <p>カード情報を読み込んでいます...</p>
            ) : (
              <div className="flex flex-wrap mt-4">
                {deckCards.map((card) => (
                  <div key={card.id} className="w-1/2 md:w-48">
                    <div className="relative w-full p-2">
                      <ImageWithSkeleton
                        src={card.image_url}
                        alt={card.detail_name}
                      />
                      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 bg-[#171717] text-center rounded-sm px-2 py-1 mb-2 w-8">
                        <div className="text-white">{card.count}</div>
                      </div>
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
