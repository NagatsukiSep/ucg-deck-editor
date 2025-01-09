"use client";

import { useState } from "react";
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

  return (
    <div className="container mx-auto p-4 ">
      <h1 className="text-2xl font-bold mb-4">デッキコード入力</h1>
      <Card>
        <CardHeader></CardHeader>
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
    </div>
  );
}
