"use client";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Search } from "lucide-react";
// import { Input } from "@/components/ui/input";
import { useState } from "react";
import { get, post } from "@/utils/request";
import { CardDetail } from "@/types/deckCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { useRouter } from "next/navigation";

type UltraHeroSearchQuery = {
  characterName: string;
  level: string;
  type: string;
  round: string;
};

const perPage = 20;

function CardComponent({
  card,
  addCard,
}: {
  card: CardDetail;
  addCard: (card: CardDetail) => void;
}) {
  const [isAdded, setIsAdded] = useState(false);

  const handleClick = () => {
    addCard(card);
    setIsAdded(true);

    // 一定時間後にスタイルをリセットする例
    setTimeout(() => {
      setIsAdded(false);
    }, 500); // 1秒後にリセット
  };

  return (
    <img
      src={card.image_url}
      alt={card.detail_name}
      className={`w-32 h-auto mx-auto cursor-pointer rounded-md  aspect-[143/200] transition-all duration-300 ${
        isAdded
          ? "outline outline-3 outline-[#171717] shadow-[0_0_15px_5px_rgba(81,81,81,0.5)] scale-105"
          : ""
      }`}
      onClick={handleClick}
    />
  );
}

export default function Home() {
  const [deckCards, setDeckCards] = useState<CardDetail[]>([]);
  const addCard = (card: CardDetail) => {
    if (deckCards.some((c) => c.id === card.id)) {
      if (deckCards.some((c) => c.id === card.id && c.count === 4)) {
        return;
      }
      setDeckCards(
        deckCards.map((c) =>
          c.id === card.id ? { ...c, count: c.count ? c.count + 1 : 2 } : c
        )
      );
      setCardCount(cardCount + 1);
    } else {
      setDeckCards([...deckCards, { ...card, count: 1 }]);
      setCardCount(cardCount + 1);
    }
  };
  const removeCard = (card: CardDetail) => {
    if (deckCards.some((c) => c.id === card.id)) {
      if (deckCards.some((c) => c.id === card.id && c.count === 1)) {
        setDeckCards(deckCards.filter((c) => c.id !== card.id));
        setCardCount(cardCount - 1);
      } else {
        setDeckCards(
          deckCards.map((c) =>
            c.id === card.id ? { ...c, count: c.count ? c.count - 1 : 0 } : c
          )
        );
        setCardCount(cardCount - 1);
      }
    }
  };
  const [cardCount, setCardCount] = useState(0);

  const [selectedGenre, setSelectedGenre] = useState("ultra-hero");
  const [searchQuery, setSearchQuery] = useState<UltraHeroSearchQuery>({
    characterName: "none",
    level: "none",
    type: "none",
    round: "none",
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
          `/search?feature_value=${searchQueryMap[selectedGenre]}&character_name=${searchQuery.characterName}&level=${searchQuery.level}&type=${searchQuery.type}&round=${searchQuery.round}&per_page=${perPage}&offset=0`
        )
      );
      const data = await get<{ total_count: number }>(
        `/search_count?feature_value=${searchQueryMap[selectedGenre]}&character_name=${searchQuery.characterName}&level=${searchQuery.level}&type=${searchQuery.type}&round=${searchQuery.round}`
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
            <div className="w-full my-4 h-[2px] bg-gray-300"></div>
            {deckCards.length > 0 ? (
              <div className="flex flex-wrap mt-4">
                {deckCards.map((card) => (
                  <div key={card.id} className="w-1/2 md:w-32">
                    <div className="relative w-full p-2">
                      <img
                        src={card.image_url}
                        alt={card.detail_name}
                        className="w-full h-auto aspect-[143/200]"
                      />
                      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 flex item-center mb-2">
                        <Button
                          onClick={() => {
                            removeCard(card);
                          }}
                          className="w-2 m-1"
                          type="submit"
                        >
                          -
                        </Button>
                        <div className="bg-[#171717] text-center rounded-sm w-8 m-1 flex items-center justify-center">
                          <div className="text-white">{card.count}</div>
                        </div>

                        <Button
                          onClick={() => {
                            addCard(card);
                          }}
                          className="w-2 m-1"
                          type="submit"
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
                  <Select
                    onValueChange={(value) =>
                      setSearchQuery({ ...searchQuery, characterName: value })
                    }
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="キャラクター名" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">キャラクター名</SelectItem>
                      <SelectItem value="アーク">アーク</SelectItem>
                      <SelectItem value="ガイア">ガイア</SelectItem>
                      <SelectItem value="ジード">ジード</SelectItem>
                      <SelectItem value="ゼット">ゼット</SelectItem>
                      <SelectItem value="ゼロ">ゼロ</SelectItem>
                      <SelectItem value="ダイナ">ダイナ</SelectItem>
                      <SelectItem value="ティガ">ティガ</SelectItem>
                      <SelectItem value="デッカー">デッカー</SelectItem>
                      <SelectItem value="トリガー">トリガー</SelectItem>
                      <SelectItem value="ブレーザー">ブレーザー</SelectItem>
                      <SelectItem value="メビウス">メビウス</SelectItem>
                    </SelectContent>
                  </Select>
                )}

                {(selectedGenre === "ultra-hero" ||
                  selectedGenre === "kaiju") && (
                  <Select
                    onValueChange={(value) =>
                      setSearchQuery({ ...searchQuery, level: value })
                    }
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="レベル" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">レベル</SelectItem>
                      <SelectItem value="1">1</SelectItem>
                      <SelectItem value="2">2</SelectItem>
                      <SelectItem value="3">3</SelectItem>
                      <SelectItem value="4">4</SelectItem>
                      <SelectItem value="5">5</SelectItem>
                      <SelectItem value="6">6</SelectItem>
                    </SelectContent>
                  </Select>
                )}

                {(selectedGenre === "ultra-hero" ||
                  selectedGenre === "kaiju") && (
                  <Select
                    onValueChange={(value) =>
                      setSearchQuery({ ...searchQuery, type: value })
                    }
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="TYPE" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">TYPE</SelectItem>
                      <SelectItem value="basic">基本</SelectItem>
                      <SelectItem value="speed">敏速</SelectItem>
                      <SelectItem value="power">剛力</SelectItem>
                      <SelectItem value="disaster">災禍</SelectItem>
                    </SelectContent>
                  </Select>
                )}

                {selectedGenre === "scene" && (
                  <Select
                    onValueChange={(value) =>
                      setSearchQuery({ ...searchQuery, round: value })
                    }
                  >
                    <SelectTrigger className="w-full">
                      <SelectValue placeholder="ラウンド" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">ラウンド</SelectItem>
                      <SelectItem value="0">0</SelectItem>
                      <SelectItem value="1">1</SelectItem>
                      <SelectItem value="2">2</SelectItem>
                      <SelectItem value="3">3</SelectItem>
                      <SelectItem value="4">4</SelectItem>
                    </SelectContent>
                  </Select>
                )}
              </div>
            </div>

            {/* <div className="w-full mt-4 flex">
            <Input
              type="text"
              placeholder="キーワードで検索"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-grow"
            />
            <Button type="submit" className="w-full sm:w-auto mx-2">
              <Search className="w-4 h-4 mr-2" />
              Search
            </Button>
          </div> */}

            <Button
              onClick={handleSearch}
              className="w-full my-4"
              type="submit"
            >
              <Search className="w-4 h-4 mr-2" />
              検索
            </Button>
            <p>検索結果: {searchedCardsCount}件</p>
            <Pagination>
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious
                    onClick={() => {
                      movePage(searchedCardsPage - 1);
                    }}
                  />
                </PaginationItem>
                {searchedCardsPage > 1 && (
                  <PaginationItem>
                    <PaginationEllipsis />
                  </PaginationItem>
                )}
                {searchedCardsPage > 0 && (
                  <PaginationItem>
                    <PaginationLink
                      onClick={() => {
                        movePage(searchedCardsPage - 1);
                      }}
                    >
                      {searchedCardsPage}
                    </PaginationLink>
                  </PaginationItem>
                )}
                <PaginationItem>
                  <PaginationLink isActive={true}>
                    {searchedCardsPage + 1}
                  </PaginationLink>
                </PaginationItem>
                {searchedCardsPage < searchedCardsCount / perPage - 1 && (
                  <PaginationItem>
                    <PaginationLink
                      onClick={() => {
                        movePage(searchedCardsPage + 1);
                      }}
                    >
                      {searchedCardsPage + 2}
                    </PaginationLink>
                  </PaginationItem>
                )}
                {searchedCardsPage < searchedCardsCount / perPage - 2 && (
                  <PaginationItem>
                    <PaginationEllipsis />
                  </PaginationItem>
                )}
                <PaginationItem>
                  <PaginationNext
                    onClick={() => {
                      movePage(searchedCardsPage + 1);
                    }}
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>

            <div className="w-full my-4 h-[2px] bg-gray-300"></div>
            {searchedCards.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-4 m-4 mx-auto">
                {searchedCards.map((card) => (
                  <div key={card.id} className="m-2">
                    <CardComponent card={card} addCard={addCard} />
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
