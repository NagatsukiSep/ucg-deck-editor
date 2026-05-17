"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { ZoomIn } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useI18n } from "@/i18n/I18nProvider";

interface ImageWithSkeletonProps {
  src: string;
  fallbackSrc?: string;
  alt: string;
  onClick?: () => void;
}

const PROXIED_IMAGE_HOSTS = new Set([
  "img.ultraman-cardgame.com",
  "api.ultraman-cardgame.com",
]);

function buildImageSrc(src: string) {
  try {
    const url = new URL(src);
    if (PROXIED_IMAGE_HOSTS.has(url.hostname)) {
      return `/api/card-image?src=${encodeURIComponent(src)}`;
    }
  } catch {
    return src;
  }

  return src;
}

export const ImageWithSkeleton = ({
  src,
  fallbackSrc,
  alt,
  onClick,
}: ImageWithSkeletonProps) => {
  const [loaded, setLoaded] = useState(false);
  const [hasTriedFallback, setHasTriedFallback] = useState(false);
  const { t } = useI18n();
  const activeSrc = hasTriedFallback && fallbackSrc ? fallbackSrc : src;
  const resolvedSrc = buildImageSrc(activeSrc);

  useEffect(() => {
    setLoaded(false);
    setHasTriedFallback(false);
  }, [src, fallbackSrc]);

  const handleError = () => {
    if (!hasTriedFallback && fallbackSrc && fallbackSrc !== src) {
      setLoaded(false);
      setHasTriedFallback(true);
      return;
    }

    setLoaded(true);
  };

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <Image
        key={resolvedSrc}
        src={resolvedSrc}
        alt={alt}
        onLoad={() => setLoaded(true)}
        onError={handleError}
        fill
        sizes="(max-width: 768px) 50vw, 143px"
        className={`object-contain transition-opacity ${
          loaded ? "opacity-100" : "opacity-0"
        }`}
        onClick={onClick}
      />
      <Dialog>
        <DialogTrigger asChild>
          <button
            type="button"
            className="absolute top-6 right-1 flex items-center justify-center w-6 h-6 p-0 text-black rounded-full bg-white/40"
            title={t("image.zoom")}
          >
            <ZoomIn className="w-5 h-5" />
          </button>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t("image.zoom")}</DialogTitle>
            <DialogDescription>{alt}</DialogDescription>
          </DialogHeader>
          <Image
            key={`zoom-${resolvedSrc}`}
            src={resolvedSrc}
            alt={alt}
            width={500}
            height={700}
            className="w-full h-auto object-contain"
          />
        </DialogContent>
      </Dialog>
      {!loaded && (
        <Skeleton className="pointer-events-none absolute inset-0 w-full h-auto aspect-[143/200]" />
      )}
    </div>
  );
};
