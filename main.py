#!/usr/bin/env python3
"""Image to ASCII art converter with CLI interface."""

import argparse
import logging
import sys
from pathlib import Path

import PIL.Image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

# ASCII gradient from darkest to lightest
ascii_chars = r".'`^\",;:Il!i<>~+_-?][}{1()|/tfjrxnvuczXYUJCQ0OZwmqdpbkhwao*#MW&8%B@$"


def validate_image_path(path: str) -> Path:
    """Validate that the image path exists and is readable."""
    image_path = Path(path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    if not image_path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    return image_path


def calculate_output_width(image: PIL.Image.Image, auto: bool, width: int | None) -> int:
    """Calculate the output width based on auto-detection or explicit width."""
    if not auto:
        return width
    
    # Guard: auto mode requires width to be None
    original_width = image.width
    
    if original_width > 2000:
        return 100
    if original_width > 1000:
        return 120
    return original_width


def resize_image(image: PIL.Image.Image, new_width: int) -> PIL.Image.Image:
    """Resize image maintaining aspect ratio with terminal character correction."""
    w, h = image.size
    # 0.55 corrects for terminal character aspect ratio (characters are taller than wide)
    new_height = int(new_width * (h / w * 0.55))
    return image.resize((new_width, new_height))


def convert_to_grayscale(image: PIL.Image.Image) -> PIL.Image.Image:
    """Convert image to grayscale."""
    return image.convert("L")


def map_pixels_to_ascii(image: PIL.Image.Image, invert: bool = False) -> str:
    """Map each pixel to an ASCII character based on brightness."""
    pixels = image.get_flattened_data()
    chars = ascii_chars
    char_count = len(chars)
    
    if invert:
        chars = chars[::-1]
    
    result = "".join(chars[pixel * (char_count - 1) // 255] for pixel in pixels)
    return result


def pixels_to_ascii_art(
    image: PIL.Image.Image,
    output_width: int,
    invert: bool = False
) -> str:
    """Convert an image to ASCII art string."""
    resized = resize_image(image, output_width)
    grayscale = convert_to_grayscale(resized)
    ascii_data = map_pixels_to_ascii(grayscale, invert)
    
    # Split into lines of exactly output_width characters
    lines = [
        ascii_data[i:i + output_width] 
        for i in range(0, len(ascii_data), output_width)
    ]
    return "\n".join(lines)


def load_image(path: str) -> PIL.Image.Image:
    """Load an image from the given path."""
    try:
        return PIL.Image.open(path)
    except IOError as e:
        raise IOError(f"Failed to open image: {e}") from e


def run_conversion(
    input_path: str,
    output_width: int | None = None,
    output_file: str | None = None,
    invert: bool = False,
    auto: bool = False
) -> str:
    """Main conversion logic - returns ASCII art string."""
    # Guard: validate input exists
    image_path = validate_image_path(input_path)
    
    # Load image
    image = load_image(str(image_path))
    
    # Calculate output width (auto-detect or use provided)
    final_width = calculate_output_width(image, auto, output_width or 120)
    
    # Convert to ASCII
    ascii_art = pixels_to_ascii_art(image, final_width, invert)
    
    return ascii_art


def main_cli() -> None:
    """CLI entry point with argparse."""
    parser = argparse.ArgumentParser(
        description="Convert images to ASCII art",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s -i photo.jpg
  %(prog)s -i photo.jpg -w 80
  %(prog)s -i photo.jpg --auto
  %(prog)s -i photo.jpg -o art.txt"""
    )
    
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to input image (required)"
    )
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=120,
        help="Output width in characters (default: 120)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save output to file (optional)"
    )
    parser.add_argument(
        "-inv", "--invert",
        action="store_true",
        help="Invert ASCII intensity (for light backgrounds)"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-detect optimal width based on image resolution"
    )
    parser.add_argument(
        "--fastfetch",
        action="store_true",
        help="Fast mode: use width=50 for quick preview"
    )
    
    args = parser.parse_args()
    
    # Handle width precedence: --fastfetch > --width > default(120)
    # --fastfetch sets width to 50, --auto uses auto-detection
    if args.fastfetch:
        final_width = 50
    elif args.auto:
        final_width = None
    else:
        final_width = args.width
    
    try:
        ascii_art = run_conversion(
            input_path=args.input,
            output_width=final_width,
            output_file=args.output,
            invert=args.invert,
            auto=args.auto
        )
        
        # Output to file or stdout
        if args.output:
            Path(args.output).write_text(ascii_art, encoding="utf-8")
            logger.info(f"Saved ASCII art to {args.output}")
        else:
            print(ascii_art)
            
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except IOError as e:
        logger.error(f"IO error: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


def interactive_mode() -> None:
    """Legacy interactive mode - kept for compatibility."""
    fondo = input("Fondo light ou dark? ").strip().lower()
    path = input("Caminho da imagem: ").strip()

    try:
        img = load_image(path)
    except (FileNotFoundError, IOError) as e:
        print(f"Erro: {e}")
        return
    
    invert = fondo == "light"
    ascii_art = pixels_to_ascii_art(img, 300, invert)
    print(ascii_art)

    if input("Salvar em .txt? (s/n): ").strip().lower() == "s":
        nome = input("Nome do arquivo: ").strip() or "ascii_art"
        try:
            Path(f"{nome}.txt").write_text(ascii_art, encoding="utf-8")
            print(f"Salvo em {nome}.txt")
        except IOError as e:
            print(f"Erro ao salvar: {e}")


if __name__ == "__main__":
    # Check if running with CLI arguments (non-interactive)
    if len(sys.argv) > 1:
        main_cli()
    else:
        interactive_mode()
