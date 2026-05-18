"use client";

import { useState } from "react";
import { CardDetail } from "@/types/deckCard";
import { ImageWithSkeleton } from "@/components/image-with-skelton";
import { ReactNode } from "react";

type Props = {
  card: CardDetail;
  addCard: (card: CardDetail, delta: number) => void;
  topLeftOverlay?: ReactNode;
};

export const CardComponent = ({ card, addCard, topLeftOverlay }: Props) => {
  const [isAdded, setIsAdded] = useState(false);

  const handleClick = () => {
    addCard(card, 1);
    setIsAdded(true);
    setTimeout(() => setIsAdded(false), 150);
  };

  return (
    <div
      className={`w-full h-auto mx-auto cursor-pointer rounded-md transition-all duration-500 ease-in-out will-change-transform will-change-filter ${
        isAdded ? "brightness-[1.5] contrast-125 scale-[1.1]" : ""
      }`}
    >
      <div className="w-full aspect-[143/200]">
        <ImageWithSkeleton
          src={card.image_url}
          fallbackSrc={card.thumbnail_image_url}
          alt={card.detail_name}
          onClick={handleClick}
          topLeftOverlay={topLeftOverlay}
        />
      </div>
    </div>
  );
};
