"use client";

import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { useI18n } from "@/i18n/I18nProvider";
import { getSavedDecks, removeDeckCode, SavedDeck } from "@/utils/myDecks";

export default function Home() {
  const [deckCode, setDeckCode] = useState("");
  const { t, locale } = useI18n();
  const [savedDecks, setSavedDecks] = useState<SavedDeck[]>([]);

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!deckCode.trim()) {
      alert(t("alerts.deckCodeRequired"));
      return;
    }
    try {
      await router.push(`/${deckCode.trim()}`);
      setDeckCode(""); // 入力欄をリセット
    } catch (error) {
      console.error("リダイレクトに失敗しました:", error);
      alert(t("alerts.redirectFailed"));
    }
  };

  type ChangelogEntry = {
    date: string;
    message:
      | string
      | {
          ja?: string;
          en?: string;
          ko?: string;
        };
  };

  const [changelog, setChangelog] = useState<ChangelogEntry[]>([]);
  const getChangelogMessage = (entry: ChangelogEntry) => {
    if (typeof entry.message === "string") {
      return entry.message;
    }
    return (
      entry.message[locale] ??
      entry.message.ja ??
      entry.message.en ??
      entry.message.ko ??
      ""
    );
  };

  useEffect(() => {
    fetch("/changelog.json")
      .then((res) => res.json())
      .then((data: ChangelogEntry[]) => setChangelog(data))
      .catch((err) =>
        console.error(t("alerts.changelogFetchFailed"), err)
      );
  }, [t]);

  useEffect(() => {
    setSavedDecks(getSavedDecks());
  }, []);

  const sortedSavedDecks = useMemo(() => {
    return [...savedDecks].sort(
      (a, b) => new Date(b.savedAt).getTime() - new Date(a.savedAt).getTime()
    );
  }, [savedDecks]);

  const handleRemoveDeck = (code: string) => {
    const nextDecks = removeDeckCode(code);
    setSavedDecks(nextDecks);
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">{t("home.myDecksTitle")}</h2>
        </CardHeader>
        <CardContent>
          {sortedSavedDecks.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              {t("home.myDecksEmpty")}
            </p>
          ) : (
            <div className="space-y-3">
              {sortedSavedDecks.map((deck) => (
                <div
                  key={deck.code}
                  className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border rounded-md p-3"
                >
                  <div>
                    <p className="text-sm font-medium">{deck.code}</p>
                    <p className="text-xs text-muted-foreground">
                      {t("home.myDecksSavedAt", {
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
                      {t("home.myDecksOpen")}
                    </Button>
                    <Button
                      type="button"
                      variant="secondary"
                      onClick={() => handleRemoveDeck(deck.code)}
                    >
                      {t("home.myDecksRemove")}
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">
            {t("home.deckCodeInputTitle")}
          </h2>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="deckCode" className="text-sm font-medium">
                {t("home.deckCodeLabel")}
              </Label>
              <Input
                id="deckCode"
                placeholder={t("home.deckCodePlaceholder")}
                value={deckCode}
                onChange={(e) => setDeckCode(e.target.value)}
                className="w-full"
              />
            </div>
            <Button type="submit" className="w-full">
              {t("home.submit")}
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">
            {t("home.newDeckTitle")}
          </h2>
        </CardHeader>
        <CardContent>
          <Button onClick={() => router.push("/new")} className="w-full">
            {t("home.newDeckButton")}
          </Button>
        </CardContent>
      </Card>

      {changelog.length > 0 && (
        <div className="mt-12 border-t pt-6 text-sm text-muted-foreground">
          <h2 className="text-base font-semibold mb-2">
            {t("home.changelogTitle")}
          </h2>
          <ul className="space-y-2 list-disc list-inside">
            {changelog.map((entry, idx) => (
              <li key={idx}>
                <span className="font-medium">{entry.date}：</span>
                {getChangelogMessage(entry)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
