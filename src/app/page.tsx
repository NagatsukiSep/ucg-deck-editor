"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { useI18n } from "@/i18n/I18nProvider";

export default function Home() {
  const [deckCode, setDeckCode] = useState("");
  const { t, locale } = useI18n();
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

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
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
