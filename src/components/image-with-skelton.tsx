import Image from "next/image";
import { useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";

interface ImageWithSkeletonProps {
  src: string;
  alt: string;
}

export const ImageWithSkeleton = ({ src, alt }: ImageWithSkeletonProps) => {
  const [loaded, setLoaded] = useState(false);
  return (
    <div className="relative w-full h-full">
      <Image
        src={src}
        alt={alt}
        width={143}
        height={200}
        onLoad={() => setLoaded(true)}
        className="w-full h-auto"
      />
      {!loaded && (
        <Skeleton className="absolute inset-0 w-full h-auto aspect-[143/200]" />
      )}
    </div>
  );
};
