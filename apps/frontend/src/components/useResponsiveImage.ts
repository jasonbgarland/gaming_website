import { useState, useEffect } from "react";

interface CoverImages {
  thumb?: string;
  small?: string;
  medium?: string;
  large?: string;
}

export function useResponsiveImage(
  coverImages: CoverImages | undefined,
  fallbackUrl?: string
) {
  const [selectedImage, setSelectedImage] = useState<string | undefined>();
  const [imageSize, setImageSize] = useState<{ width: number; height: number }>(
    { width: 227, height: 320 }
  );

  useEffect(() => {
    const selectBestImage = () => {
      if (!coverImages) {
        setSelectedImage(fallbackUrl);
        return;
      }

      // Get the current viewport width
      const viewportWidth = window.innerWidth;

      // Calculate approximate image display width based on grid layout
      let displayWidth: number;

      if (viewportWidth <= 640) {
        // Mobile: 1 column, subtract padding
        displayWidth = viewportWidth - 32; // 16px padding each side
      } else if (viewportWidth <= 768) {
        // Tablet: 2 columns
        displayWidth = (viewportWidth - 48) / 2; // 16px padding + 24px gap
      } else if (viewportWidth <= 1024) {
        // Desktop: 3 columns
        displayWidth = (viewportWidth - 64) / 3; // 16px padding + 2*24px gaps
      } else {
        // Large desktop: 3 columns but container max-width
        displayWidth = (1024 - 64) / 3; // Assuming max container width
      }

      // Select image size based on display width and device pixel ratio
      const devicePixelRatio = window.devicePixelRatio || 1;
      const targetWidth = displayWidth * devicePixelRatio;

      let selectedUrl: string | undefined;
      let width = 227,
        height = 320;

      if (targetWidth <= 90) {
        // Very small: use thumb (90x128)
        selectedUrl = coverImages.thumb;
        width = 90;
        height = 128;
      } else if (targetWidth <= 227) {
        // Small: use small (227x320)
        selectedUrl = coverImages.small;
        width = 227;
        height = 320;
      } else if (targetWidth <= 264) {
        // Medium: use medium (264x374)
        selectedUrl = coverImages.medium;
        width = 264;
        height = 374;
      } else {
        // Large: use large (1280x720 - but we'll scale it)
        selectedUrl = coverImages.large;
        width = 1280;
        height = 720;
      }

      // Fallback chain if preferred size isn't available
      selectedUrl =
        selectedUrl ||
        coverImages.large ||
        coverImages.medium ||
        coverImages.small ||
        coverImages.thumb ||
        fallbackUrl;

      setSelectedImage(selectedUrl);
      setImageSize({ width, height });
    };

    selectBestImage();

    // Listen for window resize to adjust image selection
    const handleResize = () => {
      selectBestImage();
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [coverImages, fallbackUrl]);

  return {
    selectedImage,
    imageSize,
  };
}
