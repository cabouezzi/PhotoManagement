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
    def __init__(self, path) -> None:
        self.im = Image.open(path).convert("RGBA")

    def brighten(self, factor):
        enhancer = ImageEnhance.Brightness(self.im)
        return enhancer.enhance(factor)

    def sharpen(self, factor):
        enhancer = ImageEnhance.Sharpness(self.im)
        return enhancer.enhance(factor)

    def colorize(self, factor):
        try:
            if factor > 1:
                raise ValueError
            enhancer = ImageEnhance.Color(self.im)
            return enhancer.enhance(factor)
        except ValueError:
            print("invalid value")
            return

    def contrast(self, factor):
        try:
            if factor > 1:
                raise ValueError
            enhancer = ImageEnhance.Contrast(self.im)
            return enhancer.enhance(factor)
        except ValueError:
            print("invalid value")
            return


# def increase_brightness(img, value=30):
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     h, s, v = cv2.split(hsv)

#     lim = 255 - value
#     v[v > lim] = 255
#     v[v <= lim] += value

#     final_hsv = cv2.merge((h, s, v))
#     img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
#     return img
