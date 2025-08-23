"use client";

import Image from "next/image";
import { useResponsiveImage } from "@/hooks/useResponsiveImage";

interface GameImageProps {
  coverImages?: {
    thumb?: string;
    small?: string;
    medium?: string;
    large?: string;
  };
  fallbackUrl?: string;
  alt: string;
  className?: string;
}

export function GameImage({
  coverImages,
  fallbackUrl,
  alt,
  className,
}: GameImageProps) {
  const { selectedImage, imageSize } = useResponsiveImage(
    coverImages,
    fallbackUrl
  );
  if (!selectedImage) {
    return (
      <div
        className={`bg-gamer-subtle flex items-center justify-center text-gamer-muted ${className}`}
      >
        No Image
      </div>
    );
  }

  return (
    <Image
      src={selectedImage}
      alt={alt}
      width={imageSize.width}
      height={imageSize.height}
      className={className}
      sizes="(max-width: 640px) 100vw, (max-width: 768px) 50vw, (max-width: 1024px) 33vw, 25vw"
    />
  );
}
