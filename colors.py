from colormap import rgb2hex, rgb2hls, hls2rgb, hex2rgb


def adjust_color_lightness(r, g, b, factor):
    h, l, s = rgb2hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls2rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def lighten_color(r, g, b, factor):
    return adjust_color_lightness(r, g, b, 1 + factor)


def lighten_color_hex(col, factor):
    return rgb2hex(*lighten_color(*hex2rgb(col), factor))