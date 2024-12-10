import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from PIL import Image
from gui_main import extra_fn

# from edit_type import TypeEdit

curr_img = None


class HandleImageDPG:
    def __init__(self) -> None:
        self.rgb_img = None  # Do not change this value after init
        self.result = None

    def cv2_open_img(self, path):
        with open(path, "rb") as stream:
            bytes_res = bytearray(stream.read())
            np_arr = np.asarray(bytes_res, dtype=np.uint8)
            rgb_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            self.rgb_img = rgb_img
        return rgb_img

    def delete_texture(self):
        try:
            dpg.delete_item("texture_tag")
            dpg.remove_alias("texture_tag")
            dpg.delete_item("image_tag")
        except ValueError:
            print("cannot delete texture")

    def update_texture(self, sender, app_data, user_data):
        print("updating")
        bc_img = self.bright_contra(image=self.rgb_img)
        hsv_img = self.set_hsv(image=bc_img)
        sharp = self.set_sharp(hsv_img)
        blur_img = self.blur(sharp)
        self.result = blur_img
        textureData = self.texture_to_data(blur_img)
        self.delete_texture()
        dpg.add_static_texture(
            width=hsv_img.shape[1],
            height=hsv_img.shape[0],
            default_value=textureData,
            tag="texture_tag",
            parent="texture_registry",
        )
        dpg.add_image(
            "texture_tag",
            parent="img_window",
            tag="image_tag",
            # width=int(dpg.get_item_width("texture_tag") * 0.4),
            # height=int(dpg.get_item_height("texture_tag") * 0.4),
        )
        print("done updating")

    def texture_to_data(self, image):
        auxImg = cv2.cvtColor(image, cv2.COLOR_RGB2BGRA)
        auxImg = np.asarray(auxImg, dtype="f")
        auxImg = auxImg.ravel()
        auxImg = np.true_divide(auxImg, 255.0)
        return auxImg

    def get_result(self):
        return self.result

    # def save_img(self, sender, app_data, user_data):
    #     cv2.imwrite(user_data["path"], self.result)
    #     dpg.delete_item(user_data["photo_id"] + "_texture")
    #     dpg.delete_item(user_data["photo_id"])
    #     dpg.add_static_texture(
    #         width=self.result.shape[1],
    #         height=self.result.shape[0],
    #         default_value=self.texture_to_data(self.result),
    #         tag=user_data["photo_id"] + "_texture",
    #         parent="main_texture_registry",
    #     )
    #     dpg.add_image_button(
    #         user_data["photo_id"] + "_texture",
    #         parent="image_group",
    #         tag=user_data["photo_id"],
    #         callback=extra_fn,
    #         user_data={"photo": Image.open(user_data["path"])},
    #     )

    # def get_last_active(self):
    #     for item in self.last_active:
    #         if item["status"] == True:
    #             item["status"] = False
    #             return TypeEdit[item["name"]].value
    #     return -1

    def bright_contra(self, image):
        alpha = dpg.get_value("con")
        beta = dpg.get_value("bri")
        if alpha == 1 and beta == 0:
            return image
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        # self.update_texture(user_data, new_img)

    def set_hsv(self, image):
        hue = dpg.get_value("hue")
        saturation = dpg.get_value("sat")
        if hue == 1 and saturation == 1:
            return image
        img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype("float32")
        (h, s, v) = cv2.split(img_hsv)
        h = h * hue
        h = np.clip(h, -127, 127)
        s = s * saturation
        s = np.clip(s, 0, 255)
        return cv2.cvtColor(
            cv2.merge([h, s, v]).astype("uint8"), cv2.COLOR_HSV2RGB
        )

    def set_sharp(self, image):
        sharp = dpg.get_value("sha")
        if sharp == 1:
            return image
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)

    def blur(self, image):
        dim = dpg.get_value("blur_value")
        if dpg.get_value("blur_type") == "Box":
            return cv2.blur(image, (dim, dim))
        else:
            if dim % 2 == 0:
                dim += 1
            return cv2.GaussianBlur(image, (dim, dim), 0)
