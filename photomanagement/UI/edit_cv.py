import dearpygui.dearpygui as dpg
import cv2
import numpy as np

curr_img = None


class HandleImageDPG:
    def __init__(self) -> None:
        self.img = None

    def cv2_open_img(self, path):
        with open(path, "rb") as stream:
            bytes_res = bytearray(stream.read())
            np_arr = np.asarray(bytes_res, dtype=np.uint8)
            rgba_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            self.img = rgba_img
        return rgba_img

    def delete_texture(self, texture_tag):
        try:
            dpg.delete_item(texture_tag)
            dpg.remove_alias(texture_tag)
            dpg.delete_item(texture_tag + "_img")
        except ValueError:
            print("cannot delete texture")

    def update_texture(self, texture_tag, image):
        textureData = self.texture_to_data(image)
        dpg.set_value(texture_tag, textureData)

    def texture_to_data(self, image):
        auxImg = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)
        auxImg = np.asarray(auxImg, dtype="f")
        auxImg = auxImg.ravel()
        auxImg = np.true_divide(auxImg, 255.0)
        return auxImg

    def bright_contra(self, sender, app_data, user_data):
        new_img = None
        if sender == "bright":
            new_img = cv2.convertScaleAbs(self.img, alpha=1, beta=app_data)
        else:
            new_img = cv2.convertScaleAbs(self.img, alpha=app_data, beta=0)
        self.update_texture(user_data, new_img)
