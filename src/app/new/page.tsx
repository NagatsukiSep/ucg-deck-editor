"use client";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { ChevronLeft, ChevronRight, Search } from "lucide-react";
// import { Input } from "@/components/ui/input";
import { useEffect, useState } from "react";
import { get, post } from "@/utils/request";
import { CardDetail, DeckAnalysis } from "@/types/deckCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useRouter } from "next/navigation";
import { ImageWithSkeleton } from "@/components/image-with-skelton";
import { useAppContext } from "@/context/AppContext";
import { cardTypes, kaijuCharacter, ultraCharacter } from "@/types/cardElement";
import { SearchSelect } from "@/components/searchSelect";
import { PaginationControls } from "@/components/paginationControls";
import { CardComponent } from "@/components/cardComponent";
import DeckBarChart from "@/components/deckBarChart";
import { analyzeDeck } from "@/utils/analyzeDeck";
import { Input } from "@/components/ui/input";
import { autoSortDeck, changeIndex, isEdge } from "@/utils/deckOrder";

type UltraHeroSearchQuery = {
  characterName: string;
  level: string;
  type: string;
  round: string;
  keyword?: string;
};

const perPage = 20;

export default function Home() {
  const { originalDeckCards, setOriginalDeckCards } = useAppContext();
  const [deckCards, setDeckCards] = useState<CardDetail[]>([]);
  const [deckAnalysis, setDeckAnalysis] = useState<DeckAnalysis>({});

  useEffect(() => {
    if (originalDeckCards.length > 0) {
      setDeckCards(originalDeckCards);
      setCardCount(50);
      setOriginalDeckCards([]);
      const analysis = analyzeDeck(originalDeckCards);
      setDeckAnalysis(analysis);
    }
  }, [originalDeckCards, setOriginalDeckCards]);

  const updateCardCount = (card: CardDetail, delta: number) => {
    setDeckCards((prev) => {
      const index = prev.findIndex((c) => c.id === card.id);
      if (index === -1 && delta > 0) {
        // 新規追加
        return [...prev, { ...card, count: 1 }];
      }

      if (index !== -1) {
        const current = prev[index];
        const newCount = (current.count || 1) + delta;

        if (newCount > 4) return prev; // 上限
        if (newCount <= 0) {
          // 削除
          return prev.filter((c) => c.id !== card.id);
        }

        const updated = [...prev];
        updated[index] = { ...current, count: newCount };
        return updated;
      }

      return prev;
    });
  };

  useEffect(() => {
    const total = deckCards.reduce((sum, card) => sum + (card.count || 0), 0);
    setCardCount(total);
    const analysis = analyzeDeck(deckCards);
    setDeckAnalysis(analysis);
  }, [deckCards]);

  const [cardCount, setCardCount] = useState(0);

  const [selectedGenre, setSelectedGenre] = useState("ultra-hero");
  const [searchQuery, setSearchQuery] = useState<UltraHeroSearchQuery>({
    characterName: "none",
    level: "none",
    type: "none",
    round: "none",
    keyword: "",
  });

  const searchQueryMap: Record<string, string> = {
    "ultra-hero": "ultra_hero",
    kaiju: "kaiju",
    scene: "scene",
  };

  const [searchedCardsCount, setSearchedCardsCount] = useState(0);
  const [searchedCardsPage, setSearchedCardsPage] = useState(0);
  const [searchedCards, setSearchedCards] = useState<CardDetail[]>([]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSearchedCardsPage(0);
      setSearchedCards(
        await get(
          `/search?feature_value=${searchQueryMap[selectedGenre]}&character_name=${searchQuery.characterName}&level=${searchQuery.level}&type=${searchQuery.type}&round=${searchQuery.round}&keyword=${searchQuery.keyword}&per_page=${perPage}&offset=0`
        )
      );
      const data = await get<{ total_count: number }>(
        `/search_count?feature_value=${searchQueryMap[selectedGenre]}&character_name=${searchQuery.characterName}&level=${searchQuery.level}&type=${searchQuery.type}&round=${searchQuery.round}&keyword=${searchQuery.keyword}`
      );
      setSearchedCardsCount(data[0].total_count);
    } catch (error) {
      console.error("Error fetching searched ultra hero list:", error);
    }
  };

  const movePage = async (page: number) => {
    if (page < 0 || page > searchedCardsCount / perPage) {
      return;
    }
    try {
      setSearchedCardsPage(page);
      setSearchedCards(
        await get(
          `/search?feature_value=${
            searchQueryMap[selectedGenre]
          }&character_name=${searchQuery.characterName}&level=${
            searchQuery.level
          }&type=${searchQuery.type}&round=${
            searchQuery.round
          }&per_page=${perPage}&offset=${page * perPage}`
        )
      );
    } catch (error) {
      console.error("Error fetching searched ultra hero list:", error);
    }
  };

  const router = useRouter();

  const generateDeckCode = async () => {
    if (cardCount !== 50) {
      alert("デッキは50枚でなければなりません。");
      return;
    }
    const data = {
      deck_cards: JSON.stringify(deckCards),
    };
    const response = await post<{ deck_code: string }, typeof data>(
      "new_deck",
      data
    );
    router.push(`/${response[0].deck_code}`);
    return;
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">デッキ作成</h1>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card className="p-2">
          <CardHeader>
            <CardTitle>
              <h1 className="text-2xl font-bold">現在のデッキ</h1>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <h2 className="text-xl font-bold">カード枚数: {cardCount}</h2>
            {deckCards.length > 0 && <DeckBarChart analysis={deckAnalysis} />}
            <Button
              onClick={() => {
                generateDeckCode();
              }}
              className="w-full"
              type="submit"
              disabled={cardCount !== 50}
            >
              デッキコード生成
            </Button>
            <Button
              onClick={() => {
                const sortedDeck = autoSortDeck(deckCards, deckAnalysis);
                setDeckCards(sortedDeck);
              }}
              className="w-full my-4"
              type="button"
              disabled={deckCards.length < 2}
            >
              自動並び替え
            </Button>
            <div className="w-full my-4 h-[2px] bg-gray-300"></div>
            {deckCards.length > 0 ? (
              <div className="flex flex-wrap mt-4 items-center">
                {deckCards.map((card) => (
                  <div key={card.id} className="w-1/2 md:w-32">
                    <div className="relative w-full p-2">
                      <ImageWithSkeleton
                        src={card.image_url}
                        alt={card.detail_name}
                      />
                      {!isEdge(card.id, "up", deckCards) && (
                        <div className="absolute bottom-1/2 translate-y-1/2 left-0 transform mb-2 p-2">
                          <div className="text-white bg-[#171717] rounded-sm py-1">
                            <ChevronLeft
                              onClick={() => {
                                const newDeckCards = changeIndex(
                                  card.id,
                                  "up",
                                  deckCards
                                );
                                setDeckCards(newDeckCards);
                              }}
                            />
                          </div>
                        </div>
                      )}
                      {!isEdge(card.id, "down", deckCards) && (
                        <div className="absolute bottom-1/2 translate-y-1/2 right-0 transform mb-2 p-2">
                          <div className="text-white bg-[#171717] rounded-sm py-1">
                            <ChevronRight
                              onClick={() => {
                                const newDeckCards = changeIndex(
                                  card.id,
                                  "down",
                                  deckCards
                                );
                                setDeckCards(newDeckCards);
                              }}
                            />
                          </div>
                        </div>
                      )}
                      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 flex items-center justify-center mb-2">
                        <Button
                          onClick={() => updateCardCount(card, -1)}
                          className="w-6 h-6 text-lg m-1 p-0 pb-1 rounded-full"
                          type="button"
                          disabled={(card.count ?? 0) <= 0}
                          variant="outline"
                        >
                          -
                        </Button>

                        <div className="bg-[#171717] text-white text-center rounded-sm w-8 h-8 m-1 flex items-center justify-center text-sm">
                          {card.count ?? 0}
                        </div>

                        <Button
                          onClick={() => updateCardCount(card, 1)}
                          className="w-6 h-6 text-lg m-1 p-0 rounded-full"
                          type="button"
                          disabled={(card.count ?? 0) >= 4}
                          variant={
                            (card.count ?? 0) >= 4 ? "secondary" : "outline"
                          }
                        >
                          +
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p>カードがありません。</p>
            )}
          </CardContent>
        </Card>
        <Card className="p-2">
          <CardHeader>
            <CardTitle>
              <h1 className="text-2xl font-bold">カード検索</h1>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="m-4">
              <RadioGroup
                defaultValue="ultra-hero"
                className="grid grid-cols-1 sm:grid-cols-3 gap-4"
                onValueChange={(value) => {
                  setSelectedGenre(value);
                  setSearchQuery({
                    characterName: "none",
                    level: "none",
                    type: "none",
                    round: "none",
                    keyword: "",
                  });
                }}
              >
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="ultra-hero" id="ultra-hero" />
                  <Label htmlFor="ultra-hero">ウルトラマン</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="kaiju" id="kaiju" />
                  <Label htmlFor="kaiju">ウルトラ怪獣</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="scene" id="scene" />
                  <Label htmlFor="scene">シーン</Label>
                </div>
              </RadioGroup>
            </div>

            <div className="m-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {selectedGenre === "ultra-hero" && (
                  <SearchSelect
                    label="キャラクター名"
                    value={searchQuery.characterName}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, characterName: value })
                    }
                    options={[
                      { value: "none", label: "キャラクター名" },
                      ...ultraCharacter.map((name) => ({
                        value: name,
                        label: name,
                      })),
                    ]}
                  />
                )}

                {selectedGenre === "kaiju" && (
                  <SearchSelect
                    label="キャラクター名"
                    value={searchQuery.characterName}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, characterName: value })
                    }
                    options={[
                      { value: "none", label: "キャラクター名" },
                      ...kaijuCharacter.map((name) => ({
                        value: name,
                        label: name,
                      })),
                    ]}
                  />
                )}

                {(selectedGenre === "ultra-hero" ||
                  selectedGenre === "kaiju") && (
                  <SearchSelect
                    label="レベル"
                    value={searchQuery.level}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, level: value })
                    }
                    options={[
                      { value: "none", label: "レベル" },
                      ...Array.from({ length: 7 }, (_, i) => ({
                        value: (i + 1).toString(),
                        label: (i + 1).toString(),
                      })),
                    ]}
                  />
                )}

                {(selectedGenre === "ultra-hero" ||
                  selectedGenre === "kaiju") && (
                  <SearchSelect
                    label="TYPE"
                    value={searchQuery.type}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, type: value })
                    }
                    options={[{ value: "none", label: "TYPE" }, ...cardTypes]}
                  />
                )}

                {selectedGenre === "scene" && (
                  <SearchSelect
                    label="ラウンド"
                    value={searchQuery.round}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, round: value })
                    }
                    options={[
                      { value: "none", label: "ラウンド" },
                      ...[0, 1, 2, 3, 4].map((num) => ({
                        value: num.toString(),
                        label: num.toString(),
                      })),
                    ]}
                  />
                )}
              </div>
            </div>

            <div className="w-full px-4 flex">
              <Input
                type="text"
                placeholder="キーワードで検索"
                value={searchQuery.keyword || ""}
                onChange={(e) =>
                  setSearchQuery({ ...searchQuery, keyword: e.target.value })
                }
                className="flex-grow"
              />
            </div>

            <Button
              onClick={handleSearch}
              className="w-full my-4"
              type="submit"
            >
              <Search className="w-4 h-4 mr-2" />
              検索
            </Button>
            <p>検索結果: {searchedCardsCount}件</p>
            <PaginationControls
              currentPage={searchedCardsPage}
              totalCount={searchedCardsCount}
              perPage={perPage}
              onPageChange={movePage}
            />

            <div className="w-full my-4 h-[2px] bg-gray-300"></div>
            {searchedCards.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-4 m-4 mx-auto">
                {searchedCards.map((card) => (
                  <div key={card.id} className="m-2">
                    <CardComponent
                      card={card}
                      addCard={(card, delta) => updateCardCount(card, delta)}
                    />
                  </div>
                ))}
              </div>
            ) : (
              <p>検索結果がありません。</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
