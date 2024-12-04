from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import dearpygui.dearpygui as dpg
import numpy as np

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


def load_im_array(path):
    im = Image.open(path)
    im.putalpha(255)
    res = np.array(im.getdata(), dtype=np.float32) / 255
    print(res[:5])
    return res


class ImageTransform:
    def __init__(self, path) -> None:
        self.im = Image.open(path).convert("RGBA")
        self.size = self.im.size

    def crop(self, coords):
        return self.im.crop(coords)

    def rotate(self, degree):
        return self.im.rotate(degree)

    def flip(self, method):
        if method == "lr":
            return self.im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        elif method == "tb":
            return self.im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        else:
            return self.im

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


class ImageFilterer:
    def __init__(self, path) -> None:
        self.im = Image.open(path).convert("RGBA")

    def filter(self, filter_type):
        return self.im.filter(filters[filter_type])


class ImageEnhancer:
    def __init__(self, path) -> None:
        self.im = Image.open(path).convert("RGBA")

    def enhance_fn(self, factor, enhancer_type):
        try:
            if enhancer_type not in enhancers:
                raise ValueError
            enhancer = enhancers[enhancer_type](self.im)
            return enhancer.enhance(factor)
        except ValueError:
            print("wrong type enhancer")
            return
