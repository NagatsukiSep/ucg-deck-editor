"use client";

import Image from "next/image";
import { ReactNode, useEffect, useRef, useState } from "react";
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
  actionLabel?: string;
  actionDisabled?: boolean;
  topLeftOverlay?: ReactNode;
}

const PROXIED_IMAGE_HOSTS = new Set([
  "img.ultraman-cardgame.com",
  "api.ultraman-cardgame.com",
  "tsuburaya-hk-prod.oss-accelerate.aliyuncs.com",
]);

function buildImageSrc(src: string, thumbnail = false) {

  try {
    const url = new URL(src);
    if (PROXIED_IMAGE_HOSTS.has(url.hostname)) {
      return `/api/card-image?src=${encodeURIComponent(src)}${thumbnail ? "&width=360" : ""}`;
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
  actionLabel,
  actionDisabled = false,
  topLeftOverlay,
}: ImageWithSkeletonProps) => {
  const imageRef = useRef<HTMLImageElement>(null);
  const [loaded, setLoaded] = useState(false);
  const [direct, setDirect] = useState(false);
  const [failed, setFailed] = useState(false);
  const [hasTriedFallback, setHasTriedFallback] = useState(false);
  const { t } = useI18n();
  const activeSrc = hasTriedFallback && fallbackSrc ? fallbackSrc : src;
  const resolvedSrc = direct ? activeSrc : buildImageSrc(activeSrc, true);

  useEffect(() => {
    setHasTriedFallback(false);
    setDirect(false); setFailed(false);
  }, [src, fallbackSrc]);

  useEffect(() => {
    // Cached images may already be complete before React registers onLoad.
    const image = imageRef.current;
    setLoaded(Boolean(image?.complete && image.naturalWidth > 0));
  }, [resolvedSrc]);

  const handleError = () => {
    if (!direct && resolvedSrc !== activeSrc) {
      setLoaded(false); setDirect(true); return;
    }
    if (!hasTriedFallback && fallbackSrc && fallbackSrc !== src) {
      setLoaded(false);
      setHasTriedFallback(true);
      return;
    }

    setLoaded(true); setFailed(true);
  };

  const cardImage = (
      <Image
        ref={imageRef}
        key={resolvedSrc}
        src={resolvedSrc}
        alt={alt}
        referrerPolicy="no-referrer"
        onLoad={() => setLoaded(true)}
        onError={handleError}
        fill
        sizes="120px"
        className={`object-contain transition-opacity ${
          loaded ? "opacity-100" : "opacity-0"
        }`}
      />
  );

  return (
    <div className="relative w-full aspect-[143/200] flex items-center justify-center">
      {onClick ? (
        <button type="button" onClick={onClick} disabled={actionDisabled} aria-label={actionLabel || alt} className="absolute inset-0 rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed">
          {cardImage}
        </button>
      ) : cardImage}
      {failed && <span role="status" className="pointer-events-none absolute inset-0 flex items-center justify-center bg-muted p-2 text-center text-xs">画像を読み込めませんでした</span>}
      {topLeftOverlay}
      <Dialog>
        <DialogTrigger asChild>
          <button
            type="button"
            className="absolute top-1 right-1 flex items-center justify-center w-9 h-9 md:top-6 md:w-6 md:h-6 p-0 text-black rounded-full bg-white/40"
            title={t("image.zoom")}
          >
            <ZoomIn className="w-5 h-5" />
          </button>
        </DialogTrigger>
        <DialogContent className="max-h-[95dvh] w-[calc(100%_-_2rem)] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{t("image.zoom")}</DialogTitle>
            <DialogDescription>{alt}</DialogDescription>
          </DialogHeader>
          <Image
            key={`zoom-${activeSrc}`}
            src={direct ? activeSrc : buildImageSrc(activeSrc)}
            alt={alt}
            referrerPolicy="no-referrer"
            width={500}
            height={700}
            className="mx-auto w-auto max-w-full h-auto max-h-[70dvh] object-contain"
          />
        </DialogContent>
      </Dialog>
      {!loaded && (
        <Skeleton className="pointer-events-none absolute inset-0 w-full h-full" />
      )}
    </div>
  );
};
