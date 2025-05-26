from PIL import Image

def clear_torso_layers(img: Image.Image) -> Image.Image:
    """
    Remove the outer (second) layer from the torso regions of a 64×64 Minecraft skin.
    """
    skin = img.convert('RGBA')
    mask = Image.new('RGBA', skin.size, (0, 0, 0, 0))
    clear_boxes = [
        (0, 32, 64, 48),
        (0, 32, 16, 64),
        (48, 32, 64, 64),
    ]
    for box in clear_boxes:
        skin.paste((0,0,0,0), box)
    return Image.alpha_composite(skin, mask)

def apply_jersey(base_img: Image.Image, jersey_img: Image.Image) -> Image.Image:
    """
    Takes two PIL Images (skin and jersey), composites them, and returns the result.
    """
    clean_base = clear_torso_layers(base_img)
    if jersey_img.size != clean_base.size:
        jersey_img = jersey_img.resize(clean_base.size, Image.NEAREST)
    clean_base.paste(jersey_img, (0, 0), jersey_img)
    return clean_base
