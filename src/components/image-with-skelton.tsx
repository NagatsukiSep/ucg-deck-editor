import Image from "next/image";
import { useState } from "react";
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

interface ImageWithSkeletonProps {
  src: string;
  alt: string;
  onClick?: () => void;
}

export const ImageWithSkeleton = ({
  src,
  alt,
  onClick,
}: ImageWithSkeletonProps) => {
  const [loaded, setLoaded] = useState(false);
  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <Image
        src={src}
        alt={alt}
        width={143}
        height={200}
        onLoad={() => setLoaded(true)}
        className="w-full "
        onClick={onClick}
      />
      <Dialog>
        <DialogTrigger asChild>
          <button
            type="button"
            className="absolute top-6 right-1 flex items-center justify-center w-6 h-6 p-0 text-black rounded-full bg-white/40"
            title="拡大表示"
          >
            <ZoomIn className="w-5 h-5" />
          </button>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>拡大表示</DialogTitle>
            <DialogDescription>{alt}</DialogDescription>
          </DialogHeader>
          <Image
            src={src}
            alt={alt}
            width={500}
            height={700}
            onLoad={() => setLoaded(true)}
            className="w-full h-auto"
          />
        </DialogContent>
      </Dialog>
      {!loaded && (
        <Skeleton className="absolute inset-0 w-full h-auto aspect-[143/200]" />
      )}
    </div>
  );
};
