"use client";

import Image from "next/image";
import { ReactNode, useEffect, useState } from "react";
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
  topLeftOverlay?: ReactNode;
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
  topLeftOverlay,
}: ImageWithSkeletonProps) => {
  const [loaded, setLoaded] = useState(false);
  const { t } = useI18n();
  const primarySrc = buildImageSrc(src);
  const resolvedFallbackSrc =
    fallbackSrc && fallbackSrc !== src ? buildImageSrc(fallbackSrc) : undefined;
  const [displaySrc, setDisplaySrc] = useState(primarySrc);

  useEffect(() => {
    setLoaded(false);
    setDisplaySrc(primarySrc);
  }, [primarySrc]);

  useEffect(() => {
    let active = true;
    const image = new window.Image();

    const handleLoad = () => {
      if (active) {
        setLoaded(true);
      }
    };

    const handleError = () => {
      if (!active) {
        return;
      }

      if (displaySrc === primarySrc && resolvedFallbackSrc) {
        setLoaded(false);
        setDisplaySrc(resolvedFallbackSrc);
        return;
      }

      setLoaded(true);
    };

    image.onload = handleLoad;
    image.onerror = handleError;
    image.src = displaySrc;

    if (image.complete) {
      handleLoad();
    }

    return () => {
      active = false;
      image.onload = null;
      image.onerror = null;
    };
  }, [displaySrc, primarySrc, resolvedFallbackSrc]);

  const handleError = () => {
    if (displaySrc === primarySrc && resolvedFallbackSrc) {
      setLoaded(false);
      setDisplaySrc(resolvedFallbackSrc);
      return;
    }

    setLoaded(true);
  };

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <Image
        src={displaySrc}
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
      {topLeftOverlay}
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
            src={displaySrc}
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
