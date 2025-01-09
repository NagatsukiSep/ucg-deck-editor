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

type UltraHeroSearchQuery = {
  characterName: string;
  level: string;
  type: string;
  round: string;
};

const perPage = 200;

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
    } else {
      setDeckCards([...deckCards, { ...card, count: 1 }]);
    }
  };
  const removeCard = (card: CardDetail) => {
    if (deckCards.some((c) => c.id === card.id)) {
      if (deckCards.some((c) => c.id === card.id && c.count === 1)) {
        setDeckCards(deckCards.filter((c) => c.id !== card.id));
      } else {
        setDeckCards(
          deckCards.map((c) =>
            c.id === card.id ? { ...c, count: c.count ? c.count - 1 : 0 } : c
          )
        );
      }
    }
  };
  const [deckCode, setDeckCode] = useState("");

  const [selectedGenre, setSelectedGenre] = useState("ultra-hero");
  const [searchQuery, setSearchQuery] = useState<UltraHeroSearchQuery>({
    characterName: "none",
    level: "none",
    type: "none",
    round: "none",
  });

  const [searchedCards, setSearchedCards] = useState<CardDetail[]>([]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      switch (selectedGenre) {
        case "ultra-hero":
          setSearchedCards(
            await get(
              `search_hero?character_name=${searchQuery.characterName}&level=${searchQuery.level}&type=${searchQuery.type}&per_page=${perPage}&page_number=0`
            )
          );
          break;
        case "ultra-kaiju":
          setSearchedCards(
            await get(
              `search_kaiju?level=${searchQuery.level}&type=${searchQuery.type}&per_page=${perPage}&page_number=0`
            )
          );
          break;
        case "scene":
          setSearchedCards(
            await get(
              `search_scene?round=${searchQuery.round}&per_page=${perPage}&page_number=0`
            )
          );
          break;
        default:
          break;
      }
    } catch (error) {
      console.error("Error fetching searched ultra hero list:", error);
    }
  };

  const generateDeckCode = async () => {
    const hyphenCode = deckCards
      .map((card) => {
        const count = card.count ? card.count : 1;
        return `${card.id.toString()}-${count.toString()}`;
      })
      .join("-");
    console.log(hyphenCode);
    const data = {
      deck_cards: hyphenCode,
      description: "test",
      name: "test",
    };
    const response = await post("new_deck", data);
    setDeckCode(response[0].deck_code);
    return;
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">デッキ作成</h1>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div>
          <h1 className="text-2xl font-bold mb-4">現在のデッキ</h1>
          <Button
            onClick={() => {
              generateDeckCode();
            }}
            className="w-full m-4"
            type="submit"
          >
            デッキコード生成
          </Button>
          <div>{deckCode}</div>
          <div className="w-full my-4 h-[2px] bg-gray-300"></div>
          {deckCards.length > 0 ? (
            <div className="flex flex-wrap mt-4">
              {deckCards.map((card) => (
                <div key={card.id} className="relative w-32 m-2">
                  <img
                    src={card.image_url}
                    alt={card.detail_name}
                    className="w-full h-auto"
                  />
                  <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 flex item-center">
                    <Button
                      onClick={() => {
                        addCard(card);
                      }}
                      className="w-2 m-1"
                      type="submit"
                    >
                      +
                    </Button>
                    <div className="bg-white text-center rounded-sm px-2 my-auto ">
                      <div className="my-auto">{card.count}</div>
                    </div>
                    <Button
                      onClick={() => {
                        removeCard(card);
                      }}
                      className="w-2 m-1"
                      type="submit"
                    >
                      -
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>カードがありません。</p>
          )}
        </div>
        <div>
          <h1 className="text-2xl font-bold mb-4">カード検索</h1>
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
                <RadioGroupItem value="ultra-kaiju" id="ultra-kaiju" />
                <Label htmlFor="ultra-kaiju">ウルトラ怪獣</Label>
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
                    <SelectItem value="トリガー">トリガー</SelectItem>
                    <SelectItem value="ブレーザー">ブレーザー</SelectItem>
                    <SelectItem value="メビウス">メビウス</SelectItem>
                  </SelectContent>
                </Select>
              )}

              {(selectedGenre === "ultra-hero" ||
                selectedGenre === "ultra-kaiju") && (
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
                selectedGenre === "ultra-kaiju") && (
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

          <Button onClick={handleSearch} className="w-full m-4" type="submit">
            <Search className="w-4 h-4 mr-2" />
            検索
          </Button>
          <div className="w-full my-4 h-[2px] bg-gray-300"></div>
          {searchedCards.length > 0 ? (
            <div className="flex flex-wrap mt-4 justify-center">
              {searchedCards.map((card) => (
                <div key={card.id} className="flex items-center space-x-4 m-1">
                  <img
                    src={card.image_url}
                    alt={card.detail_name}
                    className="w-32 h-auto"
                    onClick={() => {
                      addCard(card);
                    }}
                  />
                </div>
              ))}
            </div>
          ) : (
            <p>検索結果がありません。</p>
          )}
        </div>
      </div>
    </div>
  );
}
