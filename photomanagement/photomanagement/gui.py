import dearpygui.dearpygui as dpg
import math
from edit import ImageEnhancer, load_im_array
import numpy as np

# Class Init
# ----------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------------------


# Viewport
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def viewport_resize(sender, app_data):
    dpg.delete_item("widget_window")
    create_widget_group()


# ---------------------------------------------------------------------------------------------------------------------------------------------------


# choose file
# --------------------------------------------------------------------------------------------------------------------------------------------------
def choose_file_callback(_, app_data):
    print(app_data)
    path = app_data["file_path_name"]
    load_img(path)
    set_enhance_callbacks(path=path)


def load_img(path):
    try:
        width, height, channels, data = dpg.load_image(path)
        # print(np.array(data)[:5])
        # np_data = load_im_array(path)
        # print(np_data[:5])
        with dpg.texture_registry(show=True):
            dpg.add_raw_texture(
                width=width,
                height=height,
                default_value=data,
                format=dpg.mvFormat_Float_rgba,
                tag="texture_tag",
            )
        dpg.add_image("texture_tag", parent="img_window")
    except ValueError:
        print("cannot load file. path does not exist")


def choose_file_cancel(sender, app_data):
    print("Cancel was clicked.")
    print("Sender: ", sender)
    print("App Data: ", app_data)
    return


def choose_file(callback, cancel):
    idx = "file_dialog"
    file_extensions = ["jpeg", "jpg", "png", "webp", "heic"]
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=callback,
        cancel_callback=cancel,
        id=idx,
        width=700,
        height=400,
    ):
        dpg.add_file_extension(".*")
        for file_extension in file_extensions:
            dpg.add_file_extension(
                f".{file_extension}", color=(150, 255, 150, 255)
            )
    return idx


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# Set file callback
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def set_enhance_callbacks(path):
    img_enhancer = ImageEnhancer(path)

    def slider_callback(sender, app_data):
        new_img = img_enhancer.enhance_fn(app_data, sender)

        new_arr = np.array(new_img.getdata(), dtype=np.float32) / 255.0
        dpg.configure_item(
            "texture_tag",
            default_value=new_arr,
        )

    dpg.set_item_callback("bright", callback=slider_callback)
    dpg.set_item_callback("sharp", callback=slider_callback)
    dpg.set_item_callback("contrast", callback=slider_callback)
    dpg.set_item_callback("color", callback=slider_callback)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Widget
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
# def slider_callback(sender, app_data, user_data):
#     img_enhancer = ImageEnhancer(user_data)
#     new_img = img_enhancer.enhance_fn(app_data, sender)
#     new_arr = np.array(new_img.getdata(), dtype=np.float32) / 255.0
#     dpg.configure_item(
#         "texture_tag",
#         default_value=new_arr,
#     )


def create_enhancer_group():
    dpg.add_text(default_value="Enhance")
    dpg.add_slider_double(
        label="Brightness",
        default_value=1,
        tag="bright",
        min_value=0,
        max_value=5,
    )
    dpg.add_slider_double(
        label="Sharpness",
        default_value=1,
        tag="sharp",
        min_value=0,
        max_value=5,
    )
    dpg.add_slider_double(
        label="Contrast",
        clamped=True,
        min_value=0.0,
        max_value=5,
        default_value=1,
        tag="contrast",
    )
    dpg.add_slider_double(
        label="Color",
        clamped=True,
        min_value=0.0,
        max_value=5,
        default_value=1,
        tag="color",
    )


def create_resizing_group():
    dpg.add_text("Transform")
    dpg.add_button(label="Rotate")


def create_widget_group():
    with dpg.child_window(
        pos=(dpg.get_viewport_width() - 300, 30),
        tag="widget_window",
        parent="widget_window_group",
    ):
        with dpg.group(label="Enhancer"):
            create_enhancer_group()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


def main():
    dpg.create_context()
    dpg.create_viewport(title="Custom Title", resizable=True)
    dpg.set_viewport_resize_callback(callback=viewport_resize)
    with dpg.window(label="Photo Management", tag="photomanagement"):
        with dpg.menu_bar():
            d_id = choose_file(choose_file_callback, choose_file_cancel)
            dpg.add_button(
                label="add file", callback=lambda: dpg.show_item(d_id)
            )
        # Image Window
        with dpg.group(horizontal=True, tag="widget_window_tag"):
            with dpg.child_window(
                pos=(10, 30), tag="img_window", horizontal_scrollbar=True
            ):
                dpg.add_text("Some images")
        # Widget window
        with dpg.group(horizontal=True, tag="widget_window_group"):
            create_widget_group()

    dpg.setup_dearpygui()
    dpg.set_primary_window("photomanagement", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


main()
