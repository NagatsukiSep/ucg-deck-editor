"use client";

import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { ChevronLeft, ChevronRight, Images, Search } from "lucide-react";
import { useEffect, useRef, useState } from "react";
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
import { useI18n } from "@/i18n/I18nProvider";

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";

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
  const [groupSameCards, setGroupSameCards] = useState(false);
  const [artModalCard, setArtModalCard] = useState<CardDetail | null>(null);
  const [artModalMode, setArtModalMode] = useState<"view" | "select">("view");
  const [artVariants, setArtVariants] = useState<CardDetail[]>([]);
  const [deckCards, setDeckCards] = useState<CardDetail[]>([]);
  const [deckAnalysis, setDeckAnalysis] = useState<DeckAnalysis>({});
  const { t } = useI18n();
  const [characterOptions, setCharacterOptions] = useState<{feature_value: string; character_name: string}[]>([]);
  useEffect(() => {
    let active = true;
    void get<{feature_value: string; character_name: string}>("/character_options?version=2").then(rows => { if (active) setCharacterOptions(rows); }).catch(() => { /* Existing choices remain available while offline. */ });
    return () => { active = false; };
  }, []);
  const characterChoices = (feature: string, known: typeof ultraCharacter) => {
    const labels = new Map(known.map(c => [c.value, t(c.labelKey)]));
    const names = characterOptions.filter(c => c.feature_value === feature).map(c => c.character_name);
    return (names.length ? names : known.map(c => c.value)).map(name => ({value: name, label: labels.get(name) || name}));
  };

  useEffect(() => {
    if (originalDeckCards.length > 0) {
      setDeckCards(originalDeckCards);
      setCardCount(originalDeckCards.reduce((sum,c) => sum + (c.count || 0), 0));
      setOriginalDeckCards([]);
      const analysis = analyzeDeck(originalDeckCards);
      setDeckAnalysis(analysis);
    }
  }, [originalDeckCards, setOriginalDeckCards]);

  const isOverMaxCardCount = (card: CardDetail, count: number) => {
    const others = deckCards.filter(c => c.id !== card.id && c.group_key === card.group_key);
    const limit = Math.min(card.limit_count ?? 4, ...others.map(c => c.limit_count ?? 4));
    return cardCount >= 50 || count + others.reduce((sum,c) => sum + (c.count || 0), 0) > limit;
  };
  const updateCardCount = (card: CardDetail, delta: number) => {
    setDeckCards((prev) => {
      if (delta > 0) {
        if (prev.reduce((sum,c) => sum + (c.count || 0), 0) >= 50) return prev;
        const group = prev.filter(c => c.group_key === card.group_key);
        const limit = Math.min(card.limit_count ?? 4, ...group.map(c => c.limit_count ?? 4));
        if (group.reduce((sum,c) => sum + (c.count || 0), 0) + delta > limit) return prev;
      }
      const index = prev.findIndex((c) => c.id === card.id);
      if (index === -1 && delta > 0) {
        // 新規追加
        return [...prev, { ...card, count: 1 }];
      }

      if (index !== -1) {
        const current = prev[index];
        const newCount = (current.count || 1) + delta;

        if (delta > 0 && newCount > (card.limit_count ?? 4)) return prev; // 上限
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
    boost: "boost",
  };

  const [searchedCardsCount, setSearchedCardsCount] = useState(0);
  const [searchedCardsPage, setSearchedCardsPage] = useState(0);
  const [searchedCards, setSearchedCards] = useState<CardDetail[]>([]);
  const appliedQuery = useRef<string | null>(null);
  const retrySearch = useRef<{query:string; page:number} | null>(null);
  const savingRef = useRef(false);
  const [saving, setSaving] = useState(false);
  const [saveError, setSaveError] = useState("");
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState("");
  const [filtersOpen, setFiltersOpen] = useState(true);
  const searchRequest = useRef(0);
  const searchAbort = useRef<AbortController | null>(null);
  const [activePane, setActivePane] = useState<"deck" | "search">("deck");

  const runSearch = async (page = 0, grouped = groupSameCards, snapshot?: string) => {
    const requestId = ++searchRequest.current;
    searchAbort.current?.abort();
    const controller = new AbortController();
    searchAbort.current = controller;
    setSearching(true); setSearchError("");
    const query = snapshot || new URLSearchParams({version:"2", group:grouped ? "1":"0", feature_value:searchQueryMap[selectedGenre], character_name:searchQuery.characterName, level:searchQuery.level, type:searchQuery.type, round:searchQuery.round, keyword:searchQuery.keyword || ""}).toString();
    retrySearch.current = {query, page};
    try {
      const [cards, count] = await Promise.all([
        get<CardDetail>(`/search?${query}&per_page=${perPage}&offset=${page * perPage}`, {signal:controller.signal}),
        get<{total_count:number}>(`/search_count?${query}`, {signal:controller.signal})
      ]);
      if (requestId !== searchRequest.current) return;
      appliedQuery.current = query;
      setSearchedCards(cards); setSearchedCardsCount(count[0]?.total_count || 0); setSearchedCardsPage(page);
      setFiltersOpen(false);
    } catch {
      if (requestId === searchRequest.current) setSearchError("検索できませんでした。通信状況を確認して再試行してください。");
    } finally { if (requestId === searchRequest.current) setSearching(false); }
  };
  useEffect(() => () => searchAbort.current?.abort(), []);
  const handleSearch = async (e?: React.FormEvent, grouped = groupSameCards) => {
    e?.preventDefault(); await runSearch(0, grouped);
  };
  const movePage = async (page: number) => {
    if (page < 0 || page >= Math.ceil(searchedCardsCount / perPage) || searching) return;
    if (appliedQuery.current) await runSearch(page, groupSameCards, appliedQuery.current);
  };

  const openArts = async (card: CardDetail, mode: "view" | "select") => {
    setArtModalCard(card); setArtModalMode(mode); setArtVariants(card.artworks || []);
    if (!card.artworks) {
      try {
        const rows = await get<CardDetail>(`/search?version=2&keyword=${encodeURIComponent(card.code || card.detail_name)}&per_page=100`);
        setArtVariants(rows.find(c => c.group_key === card.group_key)?.artworks || [card]);
      } catch { setArtVariants([card]); }
    }
  };
  const artOverlay = (card: CardDetail, mode: "view" | "select") => (card.artwork_count ?? card.artworks?.length ?? 0) > 1 ? (
    <button type="button" className="absolute top-1 left-1 z-10 flex items-center justify-center w-9 h-9 md:top-6 md:w-6 md:h-6 p-0 text-black rounded-full bg-white/40" title={mode === "select" ? "絵柄を変更" : "絵柄一覧"} onClick={event => { event.stopPropagation(); void openArts(card, mode); }}><Images className="w-5 h-5" /></button>
  ) : undefined;

  const router = useRouter();

  const generateDeckCode = async () => {
    if (cardCount !== 50) {
      alert(t("new.alert.deckMustBe50"));
      return;
    }
    const data = {
      deck_cards: JSON.stringify(deckCards),
      card_data_version: 2,
    };
    if (savingRef.current) return;
    savingRef.current = true; setSaving(true); setSaveError("");
    try {
      const response = await post<{deck_code:string}, typeof data>("new_deck", data);
      if (!response[0]?.deck_code) throw new Error("Missing deck code");
      router.push(`/${response[0].deck_code}`);
    } catch {
      setSaveError("デッキを保存できませんでした。通信状況や枚数を確認して再試行してください。");
      savingRef.current = false; setSaving(false);
    }
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
            {t("new.mobile.deckTab")} ({cardCount}/50)
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
          <CardContent className="min-w-0 px-3 pb-3 pt-4 sm:px-6 md:pt-0">
            <h2 className="text-xl font-bold">
              {t("new.cardCount", { count: cardCount })}
            </h2>
            {deckCards.length > 0 && <DeckBarChart analysis={deckAnalysis} />}
            {saveError && <p role="alert" className="my-2 text-sm text-red-700">{saveError}</p>}
            <Button
              onClick={() => {
                generateDeckCode();
              }}
              className="w-full"
              type="submit"
              disabled={cardCount !== 50 || saving}
            >
              {saving ? "保存中…" : t("new.generateDeckCode")}
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
              <div className="card-grid mt-4">
                {deckCards.map((card) => (
                  <div key={card.id} className="w-full">
                    <div className="relative w-full aspect-[143/200]">
                      <ImageWithSkeleton
                        src={card.image_url}
                        fallbackSrc={card.thumbnail_image_url}
                        alt={card.detail_name}
                        topLeftOverlay={artOverlay(card, "select")}
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
                          className="w-9 h-9 text-lg p-0 pb-1 rounded-full md:w-6 md:h-6 md:m-1"
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
                          className="w-9 h-9 text-lg p-0 rounded-full md:w-6 md:h-6 md:m-1"
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
          <CardContent className="min-w-0 px-3 pb-3 pt-4 sm:px-6 md:pt-0">
            <Button type="button" variant="outline" className="mb-3 w-full md:hidden" aria-expanded={filtersOpen} onClick={() => setFiltersOpen(v => !v)}>検索条件を{filtersOpen ? "閉じる" : "開く"}</Button>
            <div className={filtersOpen ? "" : "hidden md:block"}>
            <div className="my-4 sm:mx-4">
              <RadioGroup
                defaultValue="ultra-hero"
                className="grid grid-cols-2 gap-3 sm:grid-cols-4"
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
                <div className="flex items-center space-x-2"><RadioGroupItem value="boost" id="boost" /><Label htmlFor="boost">ブースト</Label></div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="scene" id="scene" />
                  <Label htmlFor="scene">{t("new.genres.scene")}</Label>
                </div>
              </RadioGroup>
            </div>

            <div className="my-4 sm:mx-4">
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4 [&>*:first-child]:col-span-2 sm:[&>*:first-child]:col-span-1">
                {selectedGenre === "ultra-hero" && (
                  <SearchSelect
                    label={t("new.search.characterName")}
                    value={searchQuery.characterName}
                    onChange={(value) =>
                      setSearchQuery({ ...searchQuery, characterName: value })
                    }
                    options={[
                      { value: "none", label: t("new.search.characterName") },
                      ...characterChoices("ultra_hero", ultraCharacter),
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
                      ...characterChoices("kaiju", kaijuCharacter),
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
                      ...characterChoices("ultra_mech", ultraMechaCharacter),
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

            <div className="w-full flex flex-col gap-2 sm:flex-row sm:px-4">
              <Input
                type="text"
                placeholder={t("new.search.keywordPlaceholder")}
                value={searchQuery.keyword || ""}
                onChange={(e) =>
                  setSearchQuery({ ...searchQuery, keyword: e.target.value })
                }
                className="min-w-0 flex-grow text-base md:text-sm"
              />
              <Button type="button" variant={groupSameCards ? "default" : "outline"} className="min-h-11 shrink-0 sm:min-h-0" onClick={() => { const next = !groupSameCards; setGroupSameCards(next); void handleSearch(undefined, next); }}>同じカードをまとめる</Button>
            </div>

            <Button
              onClick={event => void handleSearch(event)}
              className="w-full my-4"
              type="submit"
            >
              <Search className="w-4 h-4 mr-2" />
              {t("new.search.action")}
            </Button>
            </div>
            {searching && <p role="status" className="my-3">検索中…</p>}
            {searchError && <div role="alert" className="my-3 text-sm text-red-700">{searchError}<Button type="button" variant="outline" onClick={() => { const retry = retrySearch.current; if (retry) void runSearch(retry.page, groupSameCards, retry.query); }}>再試行</Button></div>}
            <p>{t("new.search.results", { count: searchedCardsCount })}</p>
            <PaginationControls
              currentPage={searchedCardsPage}
              totalCount={searchedCardsCount}
              perPage={perPage}
              onPageChange={movePage}
            />

            <div className="w-full my-4 h-[2px] bg-gray-300"></div>
            {!searching && !searchError && (searchedCards.length > 0 ? (
              <div className="card-grid my-4">
                {searchedCards.map((card) => (
                  <CardComponent
                    key={card.id}
                    card={card}
                    disabled={cardCount >= 50 || isOverMaxCardCount(card, (deckCards.find(c => c.id === card.id)?.count || 0) + 1)}
                    topLeftOverlay={artOverlay(card, "view")}
                    addCard={(card, delta) => updateCardCount(card, delta)}
                  />
                ))}
              </div>
            ) : (
              <p>{t("new.search.noResults")}</p>
            ))}
          </CardContent>
        </Card>
      </div>
      <Dialog open={artModalCard !== null} onOpenChange={open => {if (!open) setArtModalCard(null);}}>
        <DialogContent className="max-h-[90dvh] w-[calc(100%_-_2rem)] overflow-y-auto"><DialogHeader><DialogTitle>{artModalMode === "select" ? "絵柄を変更" : "絵柄一覧"}</DialogTitle><DialogDescription>{artModalCard?.detail_name}</DialogDescription></DialogHeader>
          <div className="card-grid">
            {artVariants.map(art => {
              const selectArtwork = () => {
              if (!artModalCard) return;
              if (artModalMode === "view") { updateCardCount(art, 1); return; }
              const source = artModalCard;
              setDeckCards(prev => {
                if (source.id === art.id) return prev;
                const existing = prev.find(c => c.id === art.id);
                return prev.flatMap(c => c.id === source.id ? (existing ? [] : [{...art, count:c.count}]) : [{...c, count: c.id === art.id ? (c.count || 0) + (prev.find(x => x.id === source.id)?.count || 0) : c.count}]);
              }); setArtModalCard(null);
              };
              return (
                <div key={art.id} className={`rounded-md border p-2 text-left transition-colors ${artModalCard?.id === art.id ? "border-black bg-muted" : "border-border"}`}>
                  <div className="w-full aspect-[143/200]">
                    <ImageWithSkeleton src={art.image_url} fallbackSrc={art.thumbnail_image_url} alt={art.detail_name} onClick={artModalMode === "select" ? selectArtwork : undefined} />
                  </div>
                  {artModalMode === "view" ? (
                    <button type="button" className="mt-2 min-h-9 w-full rounded border text-xs disabled:text-muted-foreground" disabled={cardCount >= 50 || isOverMaxCardCount(art, (deckCards.find(c => c.id === art.id)?.count || 0) + 1)} onClick={selectArtwork}>
                      {cardCount >= 50 || isOverMaxCardCount(art, (deckCards.find(c => c.id === art.id)?.count || 0) + 1) ? "上限に達しています" : "＋ この絵柄を追加"}
                    </button>
                  ) : (
                    <button type="button" onClick={selectArtwork} className="sr-only focus:not-sr-only focus:mt-2 focus:w-full focus:rounded focus:border focus:p-1">
                      この絵柄に変更
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
