from PIL import Image, ImageOps, ImageFilter, ImageEnhance

filters = {
    "blur": ImageFilter.BLUR,
    "contour": ImageFilter.CONTOUR,
    "detail": ImageFilter.DETAIL,
    "edge enhance": ImageFilter.EDGE_ENHANCE,
    "edge enhance more": ImageFilter.EDGE_ENHANCE_MORE,
    "emboss": ImageFilter.EMBOSS,
    "find edges": ImageFilter.FIND_EDGES,
    "sharpen": ImageFilter.SHARPEN,
    "smooth": ImageFilter.SMOOTH,
    "smooth more": ImageFilter.SMOOTH_MORE,
}

enhancers = {
    "sharp": ImageEnhance.Sharpness,
    "bright": ImageEnhance.Brightness,
    "contrast": ImageEnhance.Contrast,
    "color": ImageEnhance.Color,
}


class ImageEdit:
    def __init__(self, path) -> None:
        self.im = Image.open(path)
        self.size = self.im.size

    def crop(self, coords):
        return self.im.crop(coords)

    def rotate(self, degree=45):
        return self.im.rotate(degree)

    def relative_resize(self, resize_type, pad_color="#f00"):
        try:
            match resize_type:
                case "cover":
                    return ImageOps.cover(self.im, self.size)
                case "contain":
                    return ImageOps.contain(self.im, self.size)
                case "fit":
                    return ImageOps.fit(self.im, self.size)
                case "pad":
                    return ImageOps.pad(self.im, self.size, color=pad_color)
                case _:
                    raise ValueError
        except ValueError:
            print("type does not exist.")
            return

    def filter(self, filter):
        return self.im.filter(filters[filter])


class ImageEnhancer:
    def __init__(self, path, type) -> None:
        self.im = Image.open(path)
        self.enhancer = enhancers[type](self.im)

    def enhance_noclamp(self, factor):  # for sharpness and brightness
        return self.enhancer(factor)

    def enhance_clamp(self, factor):  # for color and contrast
        try:
            if factor > 1:
                raise ValueError
            return self.enhancer(factor)
        except ValueError:
            print("invalid value")
            return
