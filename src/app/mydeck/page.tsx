"use client";

import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useI18n } from "@/i18n/I18nProvider";
import {
  getSavedDecks,
  removeDeckCode,
  SavedDeck,
  updateDeckName,
} from "@/utils/myDecks";
import { useRouter } from "next/navigation";
import { PaginationControls } from "@/components/paginationControls";

const perPage = 10;

export default function MyDeckPage() {
  const { t } = useI18n();
  const router = useRouter();
  const [savedDecks, setSavedDecks] = useState<SavedDeck[]>([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editCode, setEditCode] = useState("");
  const [editName, setEditName] = useState("");
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [deleteCode, setDeleteCode] = useState("");
  const [deleteName, setDeleteName] = useState("");

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

  const openDeleteDialog = (deck: SavedDeck) => {
    setDeleteCode(deck.code);
    setDeleteName(deck.name);
    setIsDeleteDialogOpen(true);
  };

  const handleConfirmDelete = () => {
    if (!deleteCode) {
      setIsDeleteDialogOpen(false);
      return;
    }
    handleRemoveDeck(deleteCode);
    setIsDeleteDialogOpen(false);
  };

  const openEditDialog = (deck: SavedDeck) => {
    setEditCode(deck.code);
    setEditName(deck.name);
    setIsEditDialogOpen(true);
  };

  const handleUpdateName = () => {
    if (!editName.trim()) {
      alert(t("myDeck.nameRequired"));
      return;
    }
    const nextDecks = updateDeckName(editCode, editName);
    setSavedDecks(nextDecks);
    setIsEditDialogOpen(false);
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
                      variant="outline"
                      onClick={() => openEditDialog(deck)}
                    >
                      {t("myDeck.edit")}
                    </Button>
                    <Button
                      type="button"
                      variant="destructive"
                      onClick={() => openDeleteDialog(deck)}
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
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t("myDeck.editTitle")}</DialogTitle>
            <DialogDescription>{t("myDeck.editDescription")}</DialogDescription>
          </DialogHeader>
          <div className="space-y-2">
            <label htmlFor="editDeckName" className="text-sm font-medium">
              {t("myDeck.nameLabel")}
            </label>
            <Input
              id="editDeckName"
              value={editName}
              onChange={(event) => setEditName(event.target.value)}
              placeholder={t("myDeck.namePlaceholder")}
            />
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsEditDialogOpen(false)}
            >
              {t("myDeck.cancel")}
            </Button>
            <Button type="button" onClick={handleUpdateName}>
              {t("myDeck.save")}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t("myDeck.deleteTitle")}</DialogTitle>
            <DialogDescription>{t("myDeck.deleteDescription")}</DialogDescription>
          </DialogHeader>
          <div className="space-y-1">
            <p className="text-sm font-medium">{deleteName}</p>
            <p className="text-xs text-muted-foreground">{deleteCode}</p>
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsDeleteDialogOpen(false)}
            >
              {t("myDeck.deleteCancel")}
            </Button>
            <Button type="button" variant="destructive" onClick={handleConfirmDelete}>
              {t("myDeck.deleteConfirm")}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
