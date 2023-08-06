class FontColors:
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    RESET: str = '\033[0m'


ERROR_INVALID_COLOR_CODE: str = FontColors.RED + \
    'Invalid hex color code' + FontColors.RESET


def PREVIEW_COLOR_CODE(xterm_index: int, xterm_code: str) -> str:
    preview_str: str = '        '
    result: str = "%-3d [\x1b[38;5;%dm%s\x1b[0m] : \x1b[48;5;%dm%s\x1b[0m" % (
        xterm_index,
        xterm_index,
        xterm_code,
        xterm_index,
        preview_str,
    )
    return result
