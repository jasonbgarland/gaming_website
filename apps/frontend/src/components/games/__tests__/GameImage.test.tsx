import React from "react";
import { render, screen } from "@testing-library/react";
import { GameImage } from "../GameImage";

// Mock the Next.js Image component
jest.mock("next/image", () => {
  const MockedImage = (props: React.ComponentProps<"img">) => {
    // eslint-disable-next-line @next/next/no-img-element
    return <img {...props} alt={props.alt || "mocked image"} />;
  };
  MockedImage.displayName = "MockedImage";
  return MockedImage;
});

// Mock useResponsiveImage hook
jest.mock("../../../hooks/useResponsiveImage", () => ({
  useResponsiveImage: jest.fn(),
}));

import { useResponsiveImage } from "../../../hooks/useResponsiveImage";

describe("GameImage component", () => {
  const mockUseResponsiveImage = useResponsiveImage as jest.MockedFunction<
    typeof useResponsiveImage
  >;

  beforeEach(() => {
    // Mock window properties for responsive image selection
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1024,
    });
    Object.defineProperty(window, "devicePixelRatio", {
      writable: true,
      configurable: true,
      value: 1,
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it("renders image when cover_images are provided", () => {
    const coverImages = {
      thumb: "https://images.igdb.com/igdb/image/upload/t_thumb/co1uii.jpg",
      small:
        "https://images.igdb.com/igdb/image/upload/t_cover_small/co1uii.jpg",
      medium:
        "https://images.igdb.com/igdb/image/upload/t_cover_big/co1uii.jpg",
      large: "https://images.igdb.com/igdb/image/upload/t_720p/co1uii.jpg",
    };

    mockUseResponsiveImage.mockReturnValue({
      selectedImage: coverImages.medium,
      imageSize: { width: 264, height: 374 },
    });

    render(
      <GameImage
        coverImages={coverImages}
        alt="Test Game"
        className="test-class"
      />
    );

    const image = screen.getByAltText("Test Game");
    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute("src", coverImages.medium);
  });

  it("uses fallback URL when cover_images are not provided", () => {
    const fallbackUrl =
      "https://images.igdb.com/igdb/image/upload/t_cover_big/fallback.jpg";

    mockUseResponsiveImage.mockReturnValue({
      selectedImage: fallbackUrl,
      imageSize: { width: 264, height: 374 },
    });

    render(
      <GameImage
        fallbackUrl={fallbackUrl}
        alt="Test Game"
        className="test-class"
      />
    );

    const image = screen.getByAltText("Test Game");
    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute("src", fallbackUrl);
  });

  it("renders no image placeholder when no image is available", () => {
    mockUseResponsiveImage.mockReturnValue({
      selectedImage: undefined,
      imageSize: { width: 264, height: 374 },
    });

    render(<GameImage alt="Test Game" className="test-class" />);

    expect(screen.getByText("No Image")).toBeInTheDocument();
    expect(screen.queryByAltText("Test Game")).not.toBeInTheDocument();
  });

  it("passes correct props to useResponsiveImage hook", () => {
    const coverImages = {
      thumb: "https://images.igdb.com/igdb/image/upload/t_thumb/co1uii.jpg",
      medium:
        "https://images.igdb.com/igdb/image/upload/t_cover_big/co1uii.jpg",
    };
    const fallbackUrl =
      "https://images.igdb.com/igdb/image/upload/t_cover_big/fallback.jpg";

    mockUseResponsiveImage.mockReturnValue({
      selectedImage: coverImages.medium,
      imageSize: { width: 264, height: 374 },
    });

    render(
      <GameImage
        coverImages={coverImages}
        fallbackUrl={fallbackUrl}
        alt="Test Game"
      />
    );

    expect(mockUseResponsiveImage).toHaveBeenCalledWith(
      coverImages,
      fallbackUrl
    );
  });
});
