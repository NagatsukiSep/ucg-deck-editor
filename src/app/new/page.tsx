"use client";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { ChevronLeft, ChevronRight, Images, Search } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import { get, post } from "@/utils/request";
import { CardDetail, DeckAnalysis } from "@/types/deckCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useRouter } from "next/navigation";
import { ImageWithSkeleton } from "@/components/image-with-skelton";
import { useAppContext } from "@/context/AppContext";
import {
  cardTypes,
  kaijuCharacter,
  ultraCharacter,
  ultraMechaCharacter,
} from "@/types/cardElement";
import { SearchSelect } from "@/components/searchSelect";
import { PaginationControls } from "@/components/paginationControls";
import { CardComponent } from "@/components/cardComponent";
import DeckBarChart from "@/components/deckBarChart";
import { analyzeDeck } from "@/utils/analyzeDeck";
import { Input } from "@/components/ui/input";
import { autoSortDeck, changeIndex, isEdge } from "@/utils/deckOrder";
import {
  buildArtworkGroupKey,
  fetchArtworkVariants as fetchArtworkVariantsFromApi,
} from "@/utils/cardVariants";
import {
  resolveBaseCardKey,
  serializeDeckCards,
  withBaseCardKey,
} from "@/utils/deckCardIdentity";
import { useI18n } from "@/i18n/I18nProvider";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

type UltraHeroSearchQuery = {
  characterName: string;
  level: string;
  type: string;
  round: string;
  keyword?: string;
};

const perPage = 20;
const groupedSearchFetchLimit = 2000;

const buildGroupedCardKey = (card: CardDetail) => {
  const number = resolveBaseCardKey(card);
  if (!number) {
    return card.id;
  }
  return number;
};

const groupCardsByNumberAndBranch = (cards: CardDetail[]) => {
  const grouped = new Map<string, CardDetail>();

  for (const card of cards) {
    const key = buildGroupedCardKey(card);
    const existing = grouped.get(key);
    if (!existing) {
      grouped.set(key, card);
      continue;
    }

    const existingHasBranch = Boolean(existing.branch?.trim());
    const currentHasBranch = Boolean(card.branch?.trim());

    if (existingHasBranch && !currentHasBranch) {
      grouped.set(key, card);
    }
  }

  return [...grouped.values()];
};

export default function Home() {
  const { originalDeckCards, setOriginalDeckCards } = useAppContext();
  const [deckCards, setDeckCards] = useState<CardDetail[]>([]);
  const [deckAnalysis, setDeckAnalysis] = useState<DeckAnalysis>({});
  const { t } = useI18n();

  useEffect(() => {
    if (originalDeckCards.length > 0) {
      setDeckCards(originalDeckCards.map(withBaseCardKey));
      setCardCount(50);
      setOriginalDeckCards([]);
      const analysis = analyzeDeck(originalDeckCards.map(withBaseCardKey));
      setDeckAnalysis(analysis);
    }
  }, [originalDeckCards, setOriginalDeckCards]);

  const BALTAN_RULE_IDS = ["362", "740"];

  const isOverMaxCardCount = (card: CardDetail, count: number) => {
    if (BALTAN_RULE_IDS.includes(card.id)) {
      return false;
    }
    return count > 4;
  };
  const updateCardCount = (card: CardDetail, delta: number) => {
    setDeckCards((prev) => {
      const index = prev.findIndex((c) => c.id === card.id);
      if (index === -1 && delta > 0) {
        // 新規追加
        return [...prev, { ...withBaseCardKey(card), count: 1 }];
      }

      if (index !== -1) {
        const current = prev[index];
        const newCount = (current.count || 1) + delta;

        if (isOverMaxCardCount(card, newCount)) return prev; // 上限
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
    "ultra-mecha": "ultra_mech",
    scene: "scene",
  };

  const [searchedCardsCount, setSearchedCardsCount] = useState(0);
  const [searchedCardsPage, setSearchedCardsPage] = useState(0);
  const [searchedCards, setSearchedCards] = useState<CardDetail[]>([]);
  const [groupedSearchCards, setGroupedSearchCards] = useState<CardDetail[]>([]);
  const [groupSameCards, setGroupSameCards] = useState(false);
  const [activePane, setActivePane] = useState<"deck" | "search">("deck");
  const [artModalCard, setArtModalCard] = useState<CardDetail | null>(null);
  const [artVariantCards, setArtVariantCards] = useState<CardDetail[]>([]);
  const [isArtModalLoading, setIsArtModalLoading] = useState(false);
  const [artModalMode, setArtModalMode] = useState<"select" | "view">("select");
  const [, setArtVariantCache] = useState<Record<string, CardDetail[]>>({});
  const artVariantCacheRef = useRef<Record<string, CardDetail[]>>({});
  const artworkRequestRef = useRef<Record<string, Promise<CardDetail[]>>>({});

  const buildSearchPath = (offset: number, limit: number) =>
    `/search?feature_value=${searchQueryMap[selectedGenre]}&character_name=${searchQuery.characterName}&level=${searchQuery.level}&type=${searchQuery.type}&round=${searchQuery.round}&keyword=${searchQuery.keyword}&per_page=${limit}&offset=${offset}`;

  const getCachedArtworkVariants = useCallback(
    (card: CardDetail) => artVariantCacheRef.current[buildArtworkGroupKey(card)],
    []
  );

  const runSearch = async (page: number, grouped: boolean) => {
    try {
      setSearchedCardsPage(page);

      if (grouped) {
        const cards = (await get<CardDetail>(buildSearchPath(0, groupedSearchFetchLimit))).map(
          withBaseCardKey
        );
        const dedupedCards = groupCardsByNumberAndBranch(cards);
        setGroupedSearchCards(dedupedCards);
        setSearchedCards(
          dedupedCards.slice(page * perPage, (page + 1) * perPage)
        );
        setSearchedCardsCount(dedupedCards.length);
        return;
      }

      setGroupedSearchCards([]);
      setSearchedCards(
        (await get<CardDetail>(buildSearchPath(page * perPage, perPage))).map(withBaseCardKey)
      );
      const data = await get<{ total_count: number }>(
        `/search_count?feature_value=${searchQueryMap[selectedGenre]}&character_name=${searchQuery.characterName}&level=${searchQuery.level}&type=${searchQuery.type}&round=${searchQuery.round}&keyword=${searchQuery.keyword}`
      );
      setSearchedCardsCount(data[0]?.total_count ?? 0);
    } catch (error) {
      console.error("Error fetching searched ultra hero list:", error);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    await runSearch(0, groupSameCards);
  };

  const movePage = async (page: number) => {
    if (page < 0 || page > searchedCardsCount / perPage) {
      return;
    }

    if (groupSameCards) {
      setSearchedCardsPage(page);
      setSearchedCards(groupedSearchCards.slice(page * perPage, (page + 1) * perPage));
      return;
    }

    await runSearch(page, false);
  };

  const changeDeckCardArtwork = (targetCardId: string, nextCard: CardDetail) => {
    setDeckCards((prev) => {
      const targetIndex = prev.findIndex((card) => card.id === targetCardId);
      if (targetIndex === -1) {
        return prev;
      }

      const targetCard = prev[targetIndex];
      if (targetCard.id === nextCard.id) {
        return prev;
      }

      const nextCount = targetCard.count ?? 0;
      const baseCardKey = resolveBaseCardKey(targetCard);
      const remainingCards = prev.filter((card) => card.id !== targetCardId);
      const duplicateIndex = remainingCards.findIndex((card) => card.id === nextCard.id);

      if (duplicateIndex !== -1) {
        const mergedCards = [...remainingCards];
        const duplicateCard = mergedCards[duplicateIndex];
        mergedCards[duplicateIndex] = {
          ...duplicateCard,
          count: (duplicateCard.count ?? 0) + nextCount,
        };
        return mergedCards;
      }

      const replacementCard = {
        ...withBaseCardKey(nextCard),
        base_card_key: baseCardKey,
        count: nextCount,
      };
      const updatedCards = [...remainingCards];
      updatedCards.splice(Math.min(targetIndex, updatedCards.length), 0, replacementCard);
      return updatedCards;
    });
  };

  const fetchArtworkVariants = useCallback(async (card: CardDetail) => {
    const cacheKey = buildArtworkGroupKey(card);
    const cached = artVariantCacheRef.current[cacheKey];
    if (cached) {
      return cached;
    }

    const inflight = artworkRequestRef.current[cacheKey];
    if (inflight) {
      return inflight;
    }

    const request = (async () => {
      const variants = await fetchArtworkVariantsFromApi(card);

      artVariantCacheRef.current = {
        ...artVariantCacheRef.current,
        [cacheKey]: variants,
      };
      setArtVariantCache((prev) => ({
        ...prev,
        [cacheKey]: variants,
      }));

      return variants;
    })();

    artworkRequestRef.current[cacheKey] = request;

    try {
      return await request;
    } finally {
      delete artworkRequestRef.current[cacheKey];
    }
  }, []);

  const openArtworkModal = async (card: CardDetail, mode: "select" | "view") => {
    setArtModalCard(card);
    setArtModalMode(mode);
    setArtVariantCards(getCachedArtworkVariants(card) ?? []);
    setIsArtModalLoading(true);

    try {
      const variants = await fetchArtworkVariants(card);
      setArtVariantCards(variants);
    } catch (error) {
      console.error("Error fetching artwork candidates:", error);
      setArtVariantCards([]);
    } finally {
      setIsArtModalLoading(false);
    }
  };

  useEffect(() => {
    const uniqueDeckCards = Array.from(
      new Map(deckCards.map((card) => [buildArtworkGroupKey(card), card])).values()
    );

    if (uniqueDeckCards.length === 0) {
      return;
    }

    void Promise.all(
      uniqueDeckCards.map(async (card) => {
        if (getCachedArtworkVariants(card)) {
          return;
        }
        try {
          await fetchArtworkVariants(card);
        } catch (error) {
          console.error("Error preloading artwork candidates:", error);
        }
      })
    );
  }, [deckCards, fetchArtworkVariants, getCachedArtworkVariants]);

  useEffect(() => {
    const uniqueSearchedCards = Array.from(
      new Map(searchedCards.map((card) => [buildArtworkGroupKey(card), card])).values()
    );

    if (uniqueSearchedCards.length === 0) {
      return;
    }

    void Promise.all(
      uniqueSearchedCards.map(async (card) => {
        if (getCachedArtworkVariants(card)) {
          return;
        }
        try {
          await fetchArtworkVariants(card);
        } catch (error) {
          console.error("Error preloading search artwork candidates:", error);
        }
      })
    );
  }, [searchedCards, fetchArtworkVariants, getCachedArtworkVariants]);

  const router = useRouter();

  const generateDeckCode = async () => {
    if (cardCount !== 50) {
      alert(t("new.alert.deckMustBe50"));
      return;
    }
    const data = {
      deck_cards: JSON.stringify(serializeDeckCards(deckCards)),
    };
    const response = await post<{ deck_code: string }, typeof data>(
      "new_deck",
      data
    );
    router.push(`/${response[0].deck_code}`);
    return;
  };

  return (
    <div className="container mx-auto p-4 pt-6 md:pt-4">
      <h1 className="text-2xl font-bold mb-4">{t("new.title")}</h1>
      <div className="md:hidden mb-4 sticky top-0 z-20 bg-white/95 backdrop-blur border-b border-gray-200 py-2">
        <div className="grid grid-cols-2 gap-2">
          <Button
            type="button"
            variant={activePane === "deck" ? "default" : "outline"}
            onClick={() => setActivePane("deck")}
          >
            {t("new.mobile.deckTab")}
          </Button>
          <Button
            type="button"
            variant={activePane === "search" ? "default" : "outline"}
            onClick={() => setActivePane("search")}
          >
            {t("new.mobile.searchTab")}
          </Button>
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card className={activePane === "deck" ? "p-2" : "hidden md:block p-2"}>
          <CardHeader className="hidden md:block">
            <CardTitle>
              <h1 className="text-2xl font-bold">
                {t("new.currentDeckTitle")}
              </h1>
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-4 md:pt-0">
            <h2 className="text-xl font-bold">
              {t("new.cardCount", { count: cardCount })}
            </h2>
            {deckCards.length > 0 && <DeckBarChart analysis={deckAnalysis} />}
            <Button
              onClick={() => {
                generateDeckCode();
              }}
              className="w-full"
              type="submit"
              disabled={cardCount !== 50}
            >
              {t("new.generateDeckCode")}
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
              {t("new.autoSort")}
            </Button>
            <div className="w-full my-4 h-[2px] bg-gray-300"></div>
            {deckCards.length > 0 ? (
              <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-[repeat(auto-fill,120px)] md:justify-start gap-2 sm:gap-3">
                {deckCards.map((card) => (
                  <div key={card.id} className="w-full">
                    <div className="relative w-full aspect-[143/200] p-2">
                      {(() => {
                        const variants = getCachedArtworkVariants(card);
                        const hasAlternateArts = (variants?.length ?? 0) > 1;

                        return (
                      <ImageWithSkeleton
                        src={card.image_url}
                        fallbackSrc={card.thumbnail_image_url}
                        alt={card.detail_name}
                        topLeftOverlay={hasAlternateArts ? (
                          <button
                            type="button"
                            className="absolute top-6 left-1 z-10 flex items-center justify-center w-6 h-6 p-0 text-black rounded-full bg-white/40"
                            title={t("image.changeArt")}
                            onClick={() => {
                              void openArtworkModal(card, "select");
                            }}
                          >
                            <Images className="w-5 h-5" />
                          </button>
                        ) : undefined}
                      />
                        );
                      })()}
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
                          disabled={isOverMaxCardCount(
                            card,
                            (card.count ?? 0) + 1
                          )}
                          variant={
                            isOverMaxCardCount(card, (card.count ?? 0) + 1)
                              ? "secondary"
                              : "outline"
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
              <p>{t("new.noCards")}</p>
            )}
          </CardContent>
        </Card>
        <Card
          className={activePane === "search" ? "p-2" : "hidden md:block p-2"}
        >
          <CardHeader className="hidden md:block">
            <CardTitle>
              <h1 className="text-2xl font-bold">{t("new.searchTitle")}</h1>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="m-4">
              <RadioGroup
                defaultValue="ultra-hero"
                className="grid grid-cols-1 sm:grid-cols-4 gap-4"
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
                  <Label htmlFor="ultra-hero">
                    {t("new.genres.ultraHero")}
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="ultra-mecha" id="ultra-mecha" />
                  <Label htmlFor="ultra-mecha">
                    {t("new.genres.ultraMecha")}
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="kaiju" id="kaiju" />
                  <Label htmlFor="kaiju">{t("new.genres.kaiju")}</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="scene" id="scene" />
                  <Label htmlFor="scene">{t("new.genres.scene")}</Label>
                </div>
              </RadioGroup>
            </div>

            <div className="m-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {selectedGenre === "ultra-hero" && (
                  <SearchSelect
                    label={t("new.search.characterName")}
                    value={searchQuery.characterName}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, characterName: value })
                    }
                    options={[
                      { value: "none", label: t("new.search.characterName") },
                      ...ultraCharacter.map((character) => ({
                        value: character.value,
                        label: t(character.labelKey),
                      })),
                    ]}
                  />
                )}

                {selectedGenre === "kaiju" && (
                  <SearchSelect
                    label={t("new.search.characterName")}
                    value={searchQuery.characterName}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, characterName: value })
                    }
                    options={[
                      { value: "none", label: t("new.search.characterName") },
                      ...kaijuCharacter.map((character) => ({
                        value: character.value,
                        label: t(character.labelKey),
                      })),
                    ]}
                  />
                )}

                {selectedGenre === "ultra-mecha" && (
                  <SearchSelect
                    label={t("new.search.characterName")}
                    value={searchQuery.characterName}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, characterName: value })
                    }
                    options={[
                      { value: "none", label: t("new.search.characterName") },
                      ...ultraMechaCharacter.map((character) => ({
                        value: character.value,
                        label: t(character.labelKey),
                      })),
                    ]}
                  />
                )}

                {(selectedGenre === "ultra-hero" ||
                  selectedGenre === "kaiju" ||
                  selectedGenre === "ultra-mecha") && (
                  <SearchSelect
                    label={t("new.search.level")}
                    value={searchQuery.level}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, level: value })
                    }
                    options={[
                      { value: "none", label: t("new.search.level") },
                      ...Array.from({ length: 7 }, (_, i) => ({
                        value: (i + 1).toString(),
                        label: (i + 1).toString(),
                      })),
                    ]}
                  />
                )}

                {(selectedGenre === "ultra-hero" ||
                  selectedGenre === "kaiju" ||
                  selectedGenre === "ultra-mecha") && (
                  <SearchSelect
                    label={t("new.search.type")}
                    value={searchQuery.type}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, type: value })
                    }
                    options={[
                      { value: "none", label: t("new.search.type") },
                      ...cardTypes.map((cardType) => ({
                        value: cardType.value,
                        label: t(cardType.labelKey),
                      })),
                    ]}
                  />
                )}

                {selectedGenre === "scene" && (
                  <SearchSelect
                    label={t("new.search.round")}
                    value={searchQuery.round}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, round: value })
                    }
                    options={[
                      { value: "none", label: t("new.search.round") },
                      ...[0, 1, 2, 3, 4].map((num) => ({
                        value: num.toString(),
                        label: num.toString(),
                      })),
                    ]}
                  />
                )}
              </div>
            </div>

            <div className="flex w-full gap-2 px-4">
              <Input
                type="text"
                placeholder={t("new.search.keywordPlaceholder")}
                value={searchQuery.keyword || ""}
                onChange={(e) =>
                  setSearchQuery({ ...searchQuery, keyword: e.target.value })
                }
                className="flex-grow"
              />
              <Button
                type="button"
                variant={groupSameCards ? "default" : "outline"}
                onClick={async () => {
                  const nextValue = !groupSameCards;
                  setGroupSameCards(nextValue);
                  if (searchedCards.length > 0 || searchedCardsCount > 0) {
                    await runSearch(0, nextValue);
                  }
                }}
                className="shrink-0"
              >
                {t("new.search.groupSameCards")}
              </Button>
            </div>

            <Button
              onClick={handleSearch}
              className="w-full my-4"
              type="submit"
            >
              <Search className="w-4 h-4 mr-2" />
              {t("new.search.action")}
            </Button>
            <p>{t("new.search.results", { count: searchedCardsCount })}</p>
            <PaginationControls
              currentPage={searchedCardsPage}
              totalCount={searchedCardsCount}
              perPage={perPage}
              onPageChange={movePage}
            />

            <div className="w-full my-4 h-[2px] bg-gray-300"></div>
            {searchedCards.length > 0 ? (
              <div className="m-4 mx-auto grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 md:grid-cols-[repeat(auto-fill,120px)] md:justify-start">
                {searchedCards.map((card) => {
                  const variants = getCachedArtworkVariants(card);
                  const hasAlternateArts = (variants?.length ?? 0) > 1;

                  return (
                    <CardComponent
                      key={card.id}
                      card={card}
                      addCard={(card, delta) => updateCardCount(card, delta)}
                      topLeftOverlay={hasAlternateArts ? (
                        <button
                          type="button"
                          className="absolute top-6 left-1 z-10 flex items-center justify-center w-6 h-6 p-0 text-black rounded-full bg-white/40"
                          title={t("image.viewArts")}
                          onClick={(event) => {
                            event.stopPropagation();
                            void openArtworkModal(card, "view");
                          }}
                        >
                          <Images className="w-5 h-5" />
                        </button>
                      ) : undefined}
                    />
                  );
                })}
              </div>
            ) : (
              <p>{t("new.search.noResults")}</p>
            )}
          </CardContent>
        </Card>
      </div>
      <Dialog
        open={artModalCard !== null}
        onOpenChange={(open) => {
          if (!open) {
            setArtModalCard(null);
            setArtVariantCards([]);
            setIsArtModalLoading(false);
          }
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {artModalMode === "select" ? t("image.changeArt") : t("image.viewArts")}
            </DialogTitle>
            <DialogDescription>
              {artModalCard?.detail_name ??
                (artModalMode === "select"
                  ? t("image.changeArtDescription")
                  : t("image.viewArtsDescription"))}
            </DialogDescription>
          </DialogHeader>
          {isArtModalLoading ? (
            <p>{t("image.loadingAlternates")}</p>
          ) : artVariantCards.length > 0 ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {artVariantCards.map((variant) => (
                <div
                  key={variant.id}
                  role={artModalMode === "select" ? "button" : undefined}
                  tabIndex={artModalMode === "select" ? 0 : undefined}
                  className={`rounded-md border p-2 text-left transition-colors ${
                    artModalCard?.id === variant.id
                      ? "border-black bg-muted"
                      : "border-border"
                  }`}
                  onClick={() => {
                    if (artModalMode !== "select") {
                      return;
                    }
                    if (!artModalCard) {
                      return;
                    }
                    changeDeckCardArtwork(artModalCard.id, variant);
                    setArtModalCard(null);
                    setArtVariantCards([]);
                  }}
                  onKeyDown={(event) => {
                    if (artModalMode !== "select") {
                      return;
                    }
                    if (event.key !== "Enter" && event.key !== " ") {
                      return;
                    }

                    event.preventDefault();
                    if (!artModalCard) {
                      return;
                    }
                    changeDeckCardArtwork(artModalCard.id, variant);
                    setArtModalCard(null);
                    setArtVariantCards([]);
                  }}
                >
                  <div className="w-full aspect-[143/200]">
                    <ImageWithSkeleton
                      src={variant.image_url}
                      fallbackSrc={variant.thumbnail_image_url}
                      alt={variant.detail_name}
                    />
                  </div>
                  <p className="mt-2 text-xs font-medium">
                    {variant.rarity_description || variant.number || variant.id}
                  </p>
                  {variant.number && (
                    <p className="text-[10px] text-muted-foreground">
                      {variant.number}
                    </p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p>{t("image.noAlternateArts")}</p>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
