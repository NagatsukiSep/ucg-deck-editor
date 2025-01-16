"use client";

import { CardDetail } from "@/types/deckCard";
import React, { createContext, useContext, useState, ReactNode } from "react";

// コンテキストの型定義
type AppContextType = {
  originalDeckCards: CardDetail[];
  setOriginalDeckCards: (cards: CardDetail[]) => void;
};

// 初期値を設定
const AppContext = createContext<AppContextType | undefined>(undefined);

// カスタムフック
export const useAppContext = (): AppContextType => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within an AppProvider");
  }
  return context;
};

// プロバイダーコンポーネント
export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [originalDeckCards, setOriginalDeckCards] = useState<CardDetail[]>([]);

  return (
    <AppContext.Provider value={{ originalDeckCards, setOriginalDeckCards }}>
      {children}
    </AppContext.Provider>
  );
};
