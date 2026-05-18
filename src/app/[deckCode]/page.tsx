"use client";

import DeckBarChart from "@/components/deckBarChart";
import { ImageWithSkeleton } from "@/components/image-with-skelton";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useAppContext } from "@/context/AppContext";
import { CardDetail, DeckAnalysis } from "@/types/deckCard";
import { analyzeDeck } from "@/utils/analyzeDeck";
import {
  buildArtworkGroupKey,
  fetchArtworkVariants as fetchArtworkVariantsFromApi,
} from "@/utils/cardVariants";
import {
  parseStoredDeckCards,
  withBaseCardKey,
} from "@/utils/deckCardIdentity";
import { saveDeckCode } from "@/utils/myDecks";
import { get } from "@/utils/request";
import { redirect } from "next/navigation";
import { useEffect, useState, use, useRef, useCallback } from "react";
import { useI18n } from "@/i18n/I18nProvider";
import { Images } from "lucide-react";

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
  const [isSaveDialogOpen, setIsSaveDialogOpen] = useState(false);
  const [saveName, setSaveName] = useState("");
  const [saveError, setSaveError] = useState("");
  const [artModalCard, setArtModalCard] = useState<CardDetail | null>(null);
  const [artVariantCards, setArtVariantCards] = useState<CardDetail[]>([]);
  const [isArtModalLoading, setIsArtModalLoading] = useState(false);
  const [, setArtVariantCache] = useState<Record<string, CardDetail[]>>({});
  const artVariantCacheRef = useRef<Record<string, CardDetail[]>>({});
  const artworkRequestRef = useRef<Record<string, Promise<CardDetail[]>>>({});
  const { t } = useI18n();

  const generateCollage = useCallback(
    async (cards: CardDetail[]) => {
      setIsGeneratingImage(true);
      try {
        const response = await fetch("/api/generate-image", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            images: cards.map((card) => ({
              imagePath: card.image_url,
              count: card.count,
              isScene: card.feature_value === "scene",
            })),
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
        alert(t("deck.generateImageFailed"));
      }
    },
    [t]
  );

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
      const parsed = parseStoredDeckCards(data[0].deck_cards);
      const storedCardsById = new Map(parsed.map((card) => [card.id, card]));
      const idToCount = new Map(parsed.map((card) => [card.id, card.count]));
      const cardIds = [...idToCount.keys()];
      const cardDetails = await get<CardDetail>(
        `/card_detail?ids=${cardIds.join(",")}`
      );
      const enrichedCards: CardDetail[] = cardDetails.map((card) => {
        const storedCard = storedCardsById.get(card.id);
        return withBaseCardKey({
          ...card,
          base_card_key: storedCard?.base_card_key,
          count: idToCount.get(card.id) ?? 0,
        });
      });

      // state に保存
      setDeckCards(enrichedCards);
      generateCollage(enrichedCards);
    } catch (error) {
      console.error("Failed to parse JSON:", error);
    }
    setLoadingDetails(false);
  }, [deckCode, generateCollage]);

  useEffect(() => {
    const analysis = analyzeDeck(deckCards);
    setDeckAnalysis(analysis);
  }, [deckCards]);

  useEffect(() => {
    if (didRun.current) return; // 2回目以降はスキップ
    didRun.current = true;
    getDeckData();
  }, [getDeckData]);

  const { setOriginalDeckCards } = useAppContext();
  const handleSaveDeck = () => {
    if (!saveName.trim()) {
      alert(t("deck.saveNameRequired"));
      return;
    }
    const result = saveDeckCode(deckCode, saveName);
    if (result.alreadySaved) {
      setSaveError(t("deck.saveAlready"));
      return;
    }
    if (!result.saved) {
      alert(t("deck.saveFailed"));
      return;
    }
    setSaveError("");
    setIsSaveDialogOpen(false);
  };

  const getCachedArtworkVariants = useCallback(
    (card: CardDetail) => artVariantCacheRef.current[buildArtworkGroupKey(card)],
    []
  );

  const fetchArtworkVariants = useCallback(
    async (card: CardDetail) => {
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
    },
    []
  );

  const openArtworkModal = async (card: CardDetail) => {
    setArtModalCard(card);
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

  return (
    <div className="container mx-auto p-4 ">
      <h1 className="text-2xl font-bold mb-4">{t("deck.title")}</h1>
      {is404 && (
        <div>
          <p>{t("deck.notFound")}</p>
          <Button
            onClick={() => {
              window.location.href = "/";
            }}
            className="mt-4"
          >
            {t("deck.backToTop")}
          </Button>
        </div>
      )}

      {deckCards.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>
              <h2 className="text-xl font-bold">
                {t("deck.infoTitle", { deckCode })}
              </h2>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-4 lg:flex-row lg:items-start">
              <div className="w-full min-w-0 lg:w-1/2">
                <DeckBarChart analysis={deckAnalysis} />
              </div>
              <div className="grid w-full grid-cols-1 gap-2 min-w-0 sm:grid-cols-2 lg:w-1/2">
                <Button
                  onClick={() => {
                    navigator.clipboard.writeText(deckCode);
                    alert(t("deck.copyCodeSuccess"));
                  }}
                  className="w-full"
                >
                  {t("deck.copyCode")}
                </Button>
                <Button
                  onClick={() => {
                    navigator.clipboard.writeText(
                      `${window.location.origin}/${deckCode}`
                    );
                    alert(t("deck.copyUrlSuccess"));
                  }}
                  className="w-full"
                >
                  {t("deck.copyUrl")}
                </Button>
                <Button
                  onClick={() => {
                    setSaveName(deckCode);
                    setSaveError("");
                    setIsSaveDialogOpen(true);
                  }}
                  className="w-full"
                >
                  {t("deck.saveToMyDecks")}
                </Button>
                <Button
                  onClick={() => {
                    window.open(imageUrl, "_blank");
                  }}
                  className="w-full"
                  disabled={isGeneratingImage}
                >
                  {isGeneratingImage
                    ? t("deck.loadingImage")
                    : t("deck.showImage")}
                </Button>
                <Button
                  onClick={() => {
                    setOriginalDeckCards(deckCards);
                    redirect("/new");
                  }}
                  className="w-full"
                >
                  {t("deck.fromDeck")}
                </Button>
              </div>
            </div>
            {loadingDetails ? (
              <p>{t("deck.loadingCards")}</p>
            ) : (
              <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-[repeat(auto-fit,minmax(120px,1fr))] gap-2 sm:gap-3">
                {deckCards.map((card) => (
                  <div key={card.id} className="w-full">
                    <div className="relative w-full aspect-[143/200] p-2">
                      <ImageWithSkeleton
                        src={card.image_url}
                        fallbackSrc={card.thumbnail_image_url}
                        alt={card.detail_name}
                        topLeftOverlay={
                          (getCachedArtworkVariants(card)?.length ?? 0) > 1 ? (
                            <button
                              type="button"
                              className="absolute top-6 left-1 z-10 flex items-center justify-center w-6 h-6 p-0 text-black rounded-full bg-white/40"
                              title={t("image.viewArts")}
                              onClick={() => {
                                void openArtworkModal(card);
                              }}
                            >
                              <Images className="w-5 h-5" />
                            </button>
                          ) : undefined
                        }
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
      <Dialog open={isSaveDialogOpen} onOpenChange={setIsSaveDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t("deck.saveDialogTitle")}</DialogTitle>
            <DialogDescription>
              {t("deck.saveDialogDescription")}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-2">
            <label htmlFor="saveDeckName" className="text-sm font-medium">
              {t("deck.saveDialogNameLabel")}
            </label>
            <Input
              id="saveDeckName"
              value={saveName}
              onChange={(event) => setSaveName(event.target.value)}
              placeholder={t("deck.saveDialogNamePlaceholder")}
            />
            {saveError && (
              <p className="text-sm text-red-600">{saveError}</p>
            )}
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsSaveDialogOpen(false)}
            >
              {t("deck.saveDialogCancel")}
            </Button>
            <Button type="button" onClick={handleSaveDeck}>
              {t("deck.saveDialogSave")}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      <Dialog
        open={Boolean(artModalCard)}
        onOpenChange={(open) => {
          if (open) {
            return;
          }
          setArtModalCard(null);
          setArtVariantCards([]);
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t("image.viewArts")}</DialogTitle>
            <DialogDescription>
              {artModalCard?.detail_name ?? t("image.viewArtsDescription")}
            </DialogDescription>
          </DialogHeader>
          {isArtModalLoading ? (
            <p>{t("image.loadingAlternates")}</p>
          ) : artVariantCards.length > 0 ? (
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
              {artVariantCards.map((variant) => (
                <div
                  key={variant.id}
                  className={`rounded-md border p-2 text-left transition-colors ${
                    artModalCard?.id === variant.id
                      ? "border-black bg-muted"
                      : "border-border"
                  }`}
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
