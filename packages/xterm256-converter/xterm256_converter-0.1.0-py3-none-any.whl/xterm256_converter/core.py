import os
import sys
import re
import math
import argparse

from . import message


def load_xterm256_colors() -> dict:
    # 16~255 colors
    result: dict = {}

    # load xterm256 colors file
    dir_name: str = os.path.dirname(__file__)
    file_name: str = os.path.join(dir_name, 'xterm256.csv')
    with open(file_name) as f:
        for line in f.readlines():
            line = line.replace(' ', '')
            index, code = line.split(',')
            result[int(index)] = code.strip()

    return result


def hex_to_rgb(hex_code: str) -> list:
    # [R, G, B]
    result: list = [0, 0, 0]
    hex_code = hex_code.replace('#', '')

    result[0] = int(hex_code[0:2], 16)
    result[1] = int(hex_code[2:4], 16)
    result[2] = int(hex_code[4:6], 16)

    return result


def calc_color_diff(color1: str, color2: str) -> float:
    result: float = 0.0

    # convert to [R, G, B]
    color1_rgb = hex_to_rgb(color1)
    color2_rgb = hex_to_rgb(color2)

    result = math.sqrt(
        sum([(color1_rgb[i] - color2_rgb[i]) ** 2 for i in range(3)])
    )
    return result


def main():
    # opts conf
    parser = argparse.ArgumentParser()
    parser.add_argument('color', type=str,
                        help='hex color code (no need for "#")')
    args = parser.parse_args()

    # hex color code validation
    input_color_code: str = '#' + args.color
    if not re.fullmatch(r'\#[0-9a-fA-F]{6}', input_color_code):
        print(message.ERROR_INVALID_COLOR_CODE)
        sys.exit(1)

    # load
    xterm256_colors: dict = load_xterm256_colors()

    chrom_min_diff: float = math.inf
    chrom_index: int = 0
    gray_min_diff: float = math.inf
    gray_index: int = 0
    for i in range(16, 256):
        color_diff: float = calc_color_diff(
            xterm256_colors[i],
            input_color_code,
        )

        # chromatic color
        if i < 232:
            if color_diff <= chrom_min_diff:
                chrom_min_diff = color_diff
                chrom_index = i
        # gray
        else:
            if color_diff <= gray_min_diff:
                gray_min_diff = color_diff
                gray_index = i

    # display result
    print(message.PREVIEW_COLOR_CODE(
        chrom_index,
        xterm256_colors[chrom_index],
    ))
    print(message.PREVIEW_COLOR_CODE(
        gray_index,
        xterm256_colors[gray_index],
    ))
