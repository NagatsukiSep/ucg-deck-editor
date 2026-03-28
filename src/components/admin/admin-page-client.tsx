"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
} from "@/components/ui/card";

type AdminPageClientProps = {
  authenticated: boolean;
};

export function AdminPageClient({ authenticated }: AdminPageClientProps) {
  const [password, setPassword] = useState("");
  const [importPage, setImportPage] = useState("1");
  const [promoOnly, setPromoOnly] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");
    setError("");

    if (!password.trim()) {
      setError("パスワードを入力してください。");
      return;
    }

    try {
      setIsSubmitting(true);
      const response = await fetch("/api/admin/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ password }),
      });

      const data = (await response.json()) as { error?: string };
      if (!response.ok) {
        setError(data.error ?? "認証に失敗しました。");
        return;
      }

      window.location.reload();
    } catch (loginError) {
      console.error("認証に失敗しました:", loginError);
      setError("認証に失敗しました。");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleImportCards = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");
    setError("");

    const parsedPage = Number(importPage);
    if (!Number.isInteger(parsedPage) || parsedPage < 1) {
      setError("ページ番号は 1 以上の整数で入力してください。");
      return;
    }

    try {
      setIsSubmitting(true);
      const response = await fetch("/api/admin/import-cards", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ page: parsedPage, promo: promoOnly }),
      });

      const data = (await response.json()) as {
        page?: number;
        promoOnly?: boolean;
        fetched?: number;
        beforeCount?: number;
        afterCount?: number;
        error?: string;
      };

      if (!response.ok) {
        setError(data.error ?? "カード取込に失敗しました。");
        return;
      }

      setMessage(
        `${data.promoOnly ? "プロモ" : "通常"} page ${data.page} の ${data.fetched} 件を処理しました。登録件数: ${data.beforeCount} -> ${data.afterCount}`
      );
    } catch (importError) {
      console.error("カード取込に失敗しました:", importError);
      setError("カード取込に失敗しました。");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLogout = async () => {
    try {
      setIsSubmitting(true);
      await fetch("/api/admin/logout", { method: "POST" });
      window.location.reload();
    } catch (logoutError) {
      console.error("ログアウトに失敗しました:", logoutError);
      setError("ログアウトに失敗しました。");
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto max-w-2xl px-4 py-8">
      {!authenticated ? (
        <Card>
          <CardHeader>
            <h1 className="text-2xl font-semibold">管理画面ログイン</h1>
            <CardDescription>
              管理用パスワードを入力してください。
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="adminPassword" className="text-sm font-medium">
                  パスワード
                </Label>
                <Input
                  id="adminPassword"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full"
                />
              </div>
              <Button type="submit" className="w-full" disabled={isSubmitting}>
                {isSubmitting ? "認証中..." : "ログイン"}
              </Button>
              {error && <p className="text-sm text-red-600">{error}</p>}
            </form>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <h1 className="text-2xl font-semibold">管理者カード取込</h1>
            <CardDescription>
              外部カードAPIから TiDB Cloud に取り込みます。
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleImportCards} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="importPage" className="text-sm font-medium">
                  ページ番号
                </Label>
                <Input
                  id="importPage"
                  inputMode="numeric"
                  placeholder="1"
                  value={importPage}
                  onChange={(e) => setImportPage(e.target.value)}
                  className="w-full"
                />
              </div>
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={promoOnly}
                  onChange={(e) => setPromoOnly(e.target.checked)}
                />
                プロモのみ取得する
              </label>
              <Button type="submit" className="w-full" disabled={isSubmitting}>
                {isSubmitting ? "取込中..." : "カードを取り込む"}
              </Button>
              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={handleLogout}
                disabled={isSubmitting}
              >
                ログアウト
              </Button>
              {message && <p className="text-sm text-green-600">{message}</p>}
              {error && <p className="text-sm text-red-600">{error}</p>}
            </form>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
