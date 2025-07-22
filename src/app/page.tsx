"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export default function Home() {
  const [deckCode, setDeckCode] = useState("");

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!deckCode.trim()) {
      alert("デッキコードを入力してください。");
      return;
    }
    try {
      await router.push(`/${deckCode.trim()}`);
      setDeckCode(""); // 入力欄をリセット
    } catch (error) {
      console.error("リダイレクトに失敗しました:", error);
      alert("リダイレクトに失敗しました。もう一度お試しください。");
    }
  };

  type ChangelogEntry = {
    date: string;
    message: string;
  };

  const [changelog, setChangelog] = useState<ChangelogEntry[]>([]);

  useEffect(() => {
    fetch("/changelog.json")
      .then((res) => res.json())
      .then((data: ChangelogEntry[]) => setChangelog(data))
      .catch((err) => console.error("更新ログの取得に失敗しました", err));
  }, []);

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">デッキコード入力</h2>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="deckCode" className="text-sm font-medium">
                デッキコード
              </Label>
              <Input
                id="deckCode"
                placeholder="デッキコードを入力"
                value={deckCode}
                onChange={(e) => setDeckCode(e.target.value)}
                className="w-full"
              />
            </div>
            <Button type="submit" className="w-full">
              表示する
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <h2 className="text-xl font-semibold">デッキ新規作成</h2>
        </CardHeader>
        <CardContent>
          <Button onClick={() => router.push("/new")} className="w-full">
            新規作成
          </Button>
        </CardContent>
      </Card>

      {changelog.length > 0 && (
        <div className="mt-12 border-t pt-6 text-sm text-muted-foreground">
          <h2 className="text-base font-semibold mb-2">更新ログ</h2>
          <ul className="space-y-2 list-disc list-inside">
            {changelog.map((entry, idx) => (
              <li key={idx}>
                <span className="font-medium">{entry.date}：</span>
                {entry.message}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
