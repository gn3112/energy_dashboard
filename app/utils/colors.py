import colorsys

def generate_colors(categories):
    colors_dict = {}
    for i, category in enumerate(categories):
        hue = i / len(categories)
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        colors_dict[category] = f"rgba({int(r*255)},{int(g*255)},{int(b*255)},0.6)"
    return colors_dict

def get_color(category, color_dict):
    return color_dict[category]