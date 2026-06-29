import os
from pathlib import Path


def measure_color(picture, min_background, max_black):
    from PIL import Image

    background = 0
    black = 0
    yellow = 0
    other = 0

    infile = Image.open(picture).convert("RGB")
    image = infile.load()
    xs, ys = infile.size

    for x in range(xs):
        for y in range(ys):
            r, g, b = image[x, y]

            channel_diffs = [abs(r - g), abs(r - b), abs(g - b)]

            if all(j > float(min_background) for j in [r, g, b]) and all(n < 20 for n in channel_diffs):
                background += 1
            elif all(m < max_black for m in [r, g, b]) and all(n < 20 for n in channel_diffs):
                black += 1
            elif (r - b) > 25 and (g - b) > 25 and b <= g <= r:
                yellow += 1
            else:
                other += 1

    total = black + yellow
    if total == 0:
        return [background, 0, 0, 0.0, 0, 0.0, 0.0, other]

    black_percent = round(float(black) * 100 / float(total), 2)
    yellow_percent = round(float(yellow) * 100 / float(total), 2)
    ratio = round(float(black) / float(yellow), 2) if yellow > 0 else 0.0
    return [background, total, black, black_percent, yellow, yellow_percent, ratio, other]


def run(directory, extension, background, black, output):
    header = "Sample\tBackground_pixels\tTotal_pixels\tBlack_pixels\tBlack_percent\tYellow_pixels\tYellow_percent\tRatio\tOther_pixels\n"
    results = header

    for root, dirs_list, files_list in os.walk(directory):
        for file_name in sorted(files_list):
            if os.path.splitext(file_name)[-1] == extension:
                file_path = os.path.join(root, file_name)
                row = measure_color(file_path, float(background), float(black))
                results += file_name[: file_name.index(".")] + "\t"
                results += "\t".join(str(v) for v in row)
                results += "\n"

    Path(output).write_text(results)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-directory", default=os.getcwd())
    parser.add_argument("-extension", default=".JPG")
    parser.add_argument("-background", default=120)
    parser.add_argument("-black", default=120)
    parser.add_argument("-output", default="Salamander_color_results.csv")
    args = parser.parse_args()

    run(args.directory, args.extension, args.background, args.black, args.output)
    print("Done!")
