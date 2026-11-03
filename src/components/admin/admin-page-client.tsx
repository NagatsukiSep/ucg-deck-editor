"use client";

import { useI18n } from "@/i18n/I18nProvider";
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
  const { t } = useI18n();
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
      setError(t("admin.passwordRequired"));
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

      if (!response.ok) {
        setError(t(response.status === 401 ? "admin.invalidPassword" : response.status === 403 ? "admin.forbidden" : "admin.authFailed"));
        return;
      }

      window.location.reload();
    } catch (loginError) {
      console.error("認証に失敗しました:", loginError);
      setError(t("admin.authFailed"));
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
      setError(t("admin.pageInvalid"));
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
        setError(t(response.status === 400 ? "admin.pageInvalid" : response.status === 403 ? "admin.forbidden" : "admin.importFailed"));
        return;
      }

      setMessage(
        t("admin.importSuccess", {category:t(data.promoOnly ? "admin.promo" : "admin.regular"), page:data.page ?? parsedPage, fetched:data.fetched ?? 0, before:data.beforeCount ?? 0, after:data.afterCount ?? 0})
      );
    } catch (importError) {
      console.error("カード取込に失敗しました:", importError);
      setError(t("admin.importFailed"));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLogout = async () => {
    try {
      setIsSubmitting(true);
      const response = await fetch("/api/admin/logout", { method: "POST" });
      if (!response.ok) throw new Error("Sign-out request failed");
      window.location.reload();
    } catch (logoutError) {
      console.error("ログアウトに失敗しました:", logoutError);
      setError(t("admin.logoutFailed"));
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto max-w-2xl px-4 py-8">
      {!authenticated ? (
        <Card>
          <CardHeader>
            <h1 className="text-2xl font-semibold">{t("admin.loginTitle")}</h1>
            <CardDescription>
              {t("admin.loginDescription")}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="adminPassword" className="text-sm font-medium">
                  {t("admin.password")}
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
                {isSubmitting ? t("admin.authenticating") : t("admin.login")}
              </Button>
              {error && <p className="text-sm text-red-600">{error}</p>}
            </form>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <h1 className="text-2xl font-semibold">{t("admin.title")}</h1>
            <CardDescription>
              {t("admin.description")}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleImportCards} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="importPage" className="text-sm font-medium">
                  {t("admin.page")}
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
                {t("admin.promoOnly")}
              </label>
              <Button type="submit" className="w-full" disabled={isSubmitting}>
                {isSubmitting ? t("admin.importing") : t("admin.import")}
              </Button>
              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={handleLogout}
                disabled={isSubmitting}
              >
                {t("admin.logout")}
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
