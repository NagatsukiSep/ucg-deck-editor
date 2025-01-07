"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { decodeDeck } from "@/utils/decode";
import { encodeDeck } from "@/utils/encode";
import { DeckCards } from "@/types/deckCard";

export default function Home() {
  const [deckCode, setDeckCode] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();
  const [deckCards, setDeckCards] = useState<DeckCards>({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!deckCode.trim()) {
      console.error("デッキコードを入力してください。");
      toast({
        title: "エラー",
        description: "デッキコードを入力してください。",
        variant: "destructive",
      });
      return;
    }
    setIsSubmitting(true);
    // ここでデッキコードを処理するロジックを追加します
    try {
      const deckData: DeckCards = {
        [1]: 1,
        [2]: 2,
        [3]: 3,
        [4]: 4,
        [5]: 1,
        [6]: 2,
        [7]: 3,
        [8]: 4,
        [9]: 1,
        [10]: 2,
        [11]: 3,
        [12]: 4,
      };
      const encoded = encodeDeck(deckData);
      console.log(encoded);
      // const decoded = decodeDeck(encoded);
      const decoded = decodeDeck(deckCode);
      setDeckCards(decoded);
      console.log(decoded);
    } catch (error) {
      console.error(error);
      toast({
        title: "エラー",
        description: error.message,
        variant: "destructive",
      });
    }
    setIsSubmitting(false);
    toast({
      title: "成功",
      description: `デッキコード "${deckCode}" が送信されました。`,
    });
    setDeckCode("");
  };

  return (
    <div className="container mx-auto p-4 max-w-md">
      <h1 className="text-2xl font-bold mb-4">デッキコード入力</h1>
      <p className="text-gray-600 mb-6">デッキコードを入力してください。</p>
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
        <Button type="submit" disabled={isSubmitting} className="w-full">
          {isSubmitting ? "送信中..." : "送信"}
        </Button>
      </form>
      <div className="mt-6">
        <h2 className="text-xl font-bold mb-4">デッキ情報</h2>
        <ul>
          {Object.entries(deckCards).map(([cardId, count]) => (
            <li key={cardId}>
              {cardId}: {count}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
