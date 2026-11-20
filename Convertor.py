import argparse
import numpy as np
from PIL import Image

# Наборы символов: от тёмных (плотных) к светлым
GSCALE_DETAILED = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
GSCALE_SIMPLE = "@%#*+=-:. "


def get_average_brightness(tile):
    """Возвращает среднюю яркость участка изображения (0..255)."""
    pixels = np.array(tile)
    return float(np.average(pixels))


def convert_image_to_ascii(image_path, cols=100, scale=0.43, detailed=False):
    image = Image.open(image_path).convert("L")
    width, height = image.size

    gscale = GSCALE_DETAILED if detailed else GSCALE_SIMPLE

    # Размер одного блока изображения, который станет одним символом
    tile_width = width / cols
    tile_height = tile_width / scale  # scale компенсирует то, что символы в терминале выше, чем шире
    rows = max(1, int(height / tile_height))

    ascii_rows = []
    for row in range(rows):
        y1 = int(row * tile_height)
        y2 = height if row == rows - 1 else int((row + 1) * tile_height)

        line = ""
        for col in range(cols):
            x1 = int(col * tile_width)
            x2 = width if col == cols - 1 else int((col + 1) * tile_width)

            tile = image.crop((x1, y1, x2, y2))
            avg = get_average_brightness(tile)

            # Переводим яркость 0..255 в индекс символа
            char_index = int(avg / 255 * (len(gscale) - 1))
            line += gscale[char_index]

        ascii_rows.append(line)

    return "\n".join(ascii_rows)


def main():
    while True:
        imageLink = input("Input name your image>>")
        parser = argparse.ArgumentParser(description="Конвертер изображений в ASCII-арт для терминала")
        parser.add_argument("image", nargs="?", default=imageLink, help="Путь к изображению")
        parser.add_argument("--cols", type=int, default=100, help="Ширина ASCII-арта в символах (по умолчанию: 100)")
        parser.add_argument(
        "--scale",
        type=float,
        default=0.43,
        help="Поправка на пропорции символов в терминале (по умолчанию: 0.43)",
    )
        parser.add_argument(
        "--detailed",
        action="store_true",
        help="Использовать более детальный набор символов",
    )
        args = parser.parse_args()

        ascii_art = convert_image_to_ascii(args.image, cols=args.cols, scale=args.scale, detailed=args.detailed)
        print(ascii_art)
        choice = input("end programm(Y/n)>> ")
        if choice == "Y" or choice == "y":
            break


if __name__ == "__main__":
    main()
