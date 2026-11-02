"use client";
import { OfficialDeckImport } from "@/components/official-deck-import";

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
      if (requestId === searchRequest.current) setSearchError(t("new.search.failed"));
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
    <button type="button" className="absolute top-1 left-1 z-10 flex items-center justify-center w-9 h-9 md:top-6 md:w-6 md:h-6 p-0 text-black rounded-md bg-white/85 shadow-sm hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black" title={mode === "select" ? t("image.changeArt") : t("image.viewArts")} onClick={event => { event.stopPropagation(); void openArts(card, mode); }}><Images className="w-5 h-5" /></button>
  ) : undefined;

  const router = useRouter();

  const generateDeckCode = async () => {
    setSaveError("");
    if (cardCount !== 50) {
      setSaveError(t("new.save.total", {count:cardCount}));
      return;
    }
    const groups = new Map<string, {name:string; count:number; limit:number}>();
    for (const card of deckCards) {
      const key = card.group_key || card.id;
      const previous = groups.get(key);
      groups.set(key, {name:card.detail_name, count:(previous?.count || 0) + (card.count || 0), limit:Math.min(previous?.limit ?? Infinity, card.limit_count ?? 4)});
    }
    const invalid = [...groups.values()].filter(group => group.count > group.limit);
    if (invalid.length) {
      setSaveError(invalid.map(group => t("new.save.limit", {name:group.name,count:group.count,limit:group.limit})).join("／"));
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
      setSaveError(t("new.save.failed"));
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
        <Card className={activePane === "deck" ? "min-w-0 p-2" : "hidden min-w-0 md:block p-2"}>
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
            {deckCards.length === 0 && <details className="my-4 rounded border p-3"><summary className="cursor-pointer text-sm">{t("official.expand")}</summary><div className="mt-3"><OfficialDeckImport onImport={cards => setDeckCards(cards)} /></div></details>}
            {deckCards.length > 0 && <DeckBarChart analysis={deckAnalysis} />}
            {saveError && <p role="alert" className="my-2 text-sm text-red-700">{saveError}</p>}
            <Button
              onClick={() => {
                generateDeckCode();
              }}
              className="w-full"
              type="submit"
              disabled={saving}
            >
              {saving ? t("new.saving") : t("new.generateDeckCode")}
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
              <div className="card-grid grid mt-4">
                {deckCards.map((card) => (
                  <div key={card.id} className="min-w-0 w-full">
                    <div className="relative w-full aspect-[143/200]">
                    <ImageWithSkeleton
                      src={card.image_url}
                      fallbackSrc={card.thumbnail_image_url}
                      alt={card.detail_name}
                      topLeftOverlay={artOverlay(card, "select")}
                    />
                    {!isEdge(card.id, "up", deckCards) && <button type="button" aria-label={t("card.moveBefore", {name:card.detail_name})} className="absolute left-1 top-1/2 z-10 flex h-9 w-8 -translate-y-1/2 items-center justify-center rounded-md bg-white/85 text-black shadow-sm hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black md:h-8 md:w-6" onClick={() => setDeckCards(prev => changeIndex(card.id, "up", prev))}><ChevronLeft className="h-5 w-5" /></button>}
                    {!isEdge(card.id, "down", deckCards) && <button type="button" aria-label={t("card.moveAfter", {name:card.detail_name})} className="absolute right-1 top-1/2 z-10 flex h-9 w-8 -translate-y-1/2 items-center justify-center rounded-md bg-white/85 text-black shadow-sm hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-black md:h-8 md:w-6" onClick={() => setDeckCards(prev => changeIndex(card.id, "down", prev))}><ChevronRight className="h-5 w-5" /></button>}
                    <div className="absolute bottom-1 left-1/2 z-10 w-[calc(100%_-_8px)] max-w-28 -translate-x-1/2 rounded-md bg-white/85 p-1 shadow-sm">
                      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-1">
                        <Button type="button" variant="outline" className="h-8 min-w-0 px-0 text-lg" aria-label={t("card.decrease", {name:card.detail_name})} onClick={() => updateCardCount(card, -1)}>-</Button>
                        <span className="min-w-6 text-center text-sm tabular-nums" aria-label={t("card.adopted", {count:card.count ?? 0})}>{card.count ?? 0}</span>
                        <Button type="button" variant="outline" className="h-8 min-w-0 px-0 text-lg" aria-label={t("card.increase", {name:card.detail_name})} onClick={() => updateCardCount(card, 1)}>+</Button>
                      </div>
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
            <Button type="button" variant="outline" className="mb-3 w-full md:hidden" aria-expanded={filtersOpen} onClick={() => setFiltersOpen(v => !v)}>{t(filtersOpen ? "new.search.closeFilters" : "new.search.openFilters")}</Button>
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
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="scene" id="scene" />
                  <Label htmlFor="scene">{t("new.genres.scene")}</Label>
                </div>
                <div className="flex items-center space-x-2"><RadioGroupItem value="boost" id="boost" /><Label htmlFor="boost">{t("new.genres.boost")}</Label></div>
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
              <Button type="button" variant={groupSameCards ? "default" : "outline"} className="min-h-11 shrink-0 sm:min-h-0" onClick={() => { const next = !groupSameCards; setGroupSameCards(next); void handleSearch(undefined, next); }}>{t("new.search.groupSameCards")}</Button>
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
            {searching && <p role="status" className="my-3">{t("new.search.loading")}</p>}
            {searchError && <div role="alert" className="my-3 text-sm text-red-700">{searchError}<Button type="button" variant="outline" onClick={() => { const retry = retrySearch.current; if (retry) void runSearch(retry.page, groupSameCards, retry.query); }}>{t("common.retry")}</Button></div>}
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
        <DialogContent className="max-h-[90dvh] w-[calc(100%_-_2rem)] overflow-y-auto"><DialogHeader><DialogTitle>{artModalMode === "select" ? t("image.changeArt") : t("image.viewArts")}</DialogTitle><DialogDescription>{artModalCard?.detail_name}</DialogDescription></DialogHeader>
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
                    <button type="button" className="mt-2 min-h-9 w-full rounded border text-xs disabled:text-muted-foreground" onClick={selectArtwork}>
                      {t("image.addArt")}
                    </button>
                  ) : (
                    <button type="button" onClick={selectArtwork} className="sr-only focus:not-sr-only focus:mt-2 focus:w-full focus:rounded focus:border focus:p-1">
                      {t("image.selectArt")}
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
