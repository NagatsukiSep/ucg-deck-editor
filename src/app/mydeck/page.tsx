"use client";

import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { useI18n } from "@/i18n/I18nProvider";
import { getSavedDecks, removeDeckCode, SavedDeck } from "@/utils/myDecks";
import { useRouter } from "next/navigation";
import { PaginationControls } from "@/components/paginationControls";

const perPage = 10;

export default function MyDeckPage() {
  const { t } = useI18n();
  const router = useRouter();
  const [savedDecks, setSavedDecks] = useState<SavedDeck[]>([]);
  const [currentPage, setCurrentPage] = useState(0);

  useEffect(() => {
    setSavedDecks(getSavedDecks());
  }, []);

  const sortedSavedDecks = useMemo(() => {
    return [...savedDecks].sort(
      (a, b) => new Date(b.savedAt).getTime() - new Date(a.savedAt).getTime()
    );
  }, [savedDecks]);

  useEffect(() => {
    const totalPages = Math.max(1, Math.ceil(sortedSavedDecks.length / perPage));
    if (currentPage > totalPages - 1) {
      setCurrentPage(totalPages - 1);
    }
  }, [currentPage, sortedSavedDecks.length]);

  const handleRemoveDeck = (code: string) => {
    const nextDecks = removeDeckCode(code);
    setSavedDecks(nextDecks);
  };

  const pagedDecks = useMemo(() => {
    const start = currentPage * perPage;
    return sortedSavedDecks.slice(start, start + perPage);
  }, [currentPage, sortedSavedDecks]);

  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">{t("myDeck.title")}</h2>
        </CardHeader>
        <CardContent>
          {sortedSavedDecks.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              {t("myDeck.empty")}
            </p>
          ) : (
            <div className="space-y-3">
              {pagedDecks.map((deck) => (
                <div
                  key={deck.code}
                  className="flex flex-col gap-2 border rounded-md p-3 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div>
                    <p className="text-sm font-medium">{deck.name}</p>
                    <p className="text-xs text-muted-foreground">{deck.code}</p>
                    <p className="text-xs text-muted-foreground">
                      {t("myDeck.savedAt", {
                        date: new Date(deck.savedAt).toLocaleString(),
                      })}
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => router.push(`/${deck.code}`)}
                    >
                      {t("myDeck.open")}
                    </Button>
                    <Button
                      type="button"
                      variant="secondary"
                      onClick={() => handleRemoveDeck(deck.code)}
                    >
                      {t("myDeck.remove")}
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {sortedSavedDecks.length > perPage && (
        <PaginationControls
          currentPage={currentPage}
          totalCount={sortedSavedDecks.length}
          perPage={perPage}
          onPageChange={setCurrentPage}
        />
      )}
    </div>
  );
}
