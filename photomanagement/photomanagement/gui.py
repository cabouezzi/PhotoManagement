import dearpygui.dearpygui as dpg
import math
from edit import ImageEnhancer, ImageTransform
import numpy as np


# Viewport
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def viewport_resize(sender, app_data):
    dpg.delete_item("widget_window")
    create_widget_group()


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# choose file
# --------------------------------------------------------------------------------------------------------------------------------------------------
def choose_file_callback(_, app_data):
    path = app_data["file_path_name"]
    load_img(path)
    set_enhance_callbacks(path=path)
    set_transform_callbacks(path=path)


def load_img(path):
    width, height, channels, data = dpg.load_image(path)
    try:
        # when there is path
        if dpg.get_value("img_path") != "Path ":
            # width, height, channels, data = dpg.load_image(path)
            dpg.delete_item("texture_tag")
            dpg.remove_alias("texture_tag")
            dpg.delete_item("image_tag")
        with dpg.texture_registry(show=True):
            dpg.add_raw_texture(
                width=width,
                height=height,
                default_value=data,
                format=dpg.mvFormat_Float_rgba,
                tag="texture_tag",
            )
            dpg.add_image("texture_tag", parent="img_window", tag="image_tag")
            dpg.set_value("img_path", value=f"Path {path}")
    except ValueError:
        print("cannot load file. path does not exist")


def choose_file(callback):
    idx = "file_dialog"
    file_extensions = ["jpeg", "jpg", "png", "webp", "heic"]
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=callback,
        id=idx,
        width=700,
        height=400,
    ):
        for file_extension in file_extensions:
            dpg.add_file_extension(
                f".{file_extension}", color=(150, 255, 150, 255)
            )
    return idx

    # ---------------------------------------------------------------------------------------------------------------------------------------------------
    # Set file callback
    # ---------------------------------------------------------------------------------------------------------------------------------------------------


def set_enhance_callbacks(path):
    enhance_tags = ["bright", "sharp", "contrast", "color"]
    img_enhancer = ImageEnhancer(path)

    def slider_callback(sender, app_data):
        new_img = img_enhancer.enhance_fn(app_data, sender)
        new_arr = np.array(new_img.getdata(), dtype=np.float32) / 255.0
        dpg.configure_item(
            "texture_tag",
            default_value=new_arr,
        )

    for tag in enhance_tags:
        dpg.set_item_callback(tag, callback=slider_callback)


def set_transform_callbacks(path):
    transform_tags = ["rotate", "lr", "tb"]
    img_transformer = ImageTransform(path)

    def transform_callback(sender, app_data):
        if sender == "rotate":
            new_img = img_transformer.rotate(app_data)
        elif sender in ("lr", "tb"):
            new_img = img_transformer.flip(sender)
        new_arr = np.array(new_img.getdata(), dtype=np.float32) / 255.0
        dpg.configure_item(
            "texture_tag",
            default_value=new_arr,
            width=new_img.width,
            height=new_img.height,
        )

    for tag in transform_tags:
        dpg.set_item_callback(tag, callback=transform_callback)


def reset_img():
    path_value = str(dpg.get_value("img_path")).split()
    if len(path_value) > 1:
        width, height, channels, data = dpg.load_image(path_value[1])
        dpg.configure_item(
            "texture_tag",
            default_value=data,
        )


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Widget
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------


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


def create_transform_group():
    dpg.add_text("Transform")
    dpg.add_input_int(label="Rotate", tag="rotate", min_value=0, max_value=360)
    # dpg.add_combo(
    #     label="Resize",
    #     items=["cover", "contain", "fit", "pad"],
    #     tag="resize_dropdown",
    # )
    dpg.add_button(label="Flip Left-Right", tag="lr")
    dpg.add_button(label="Flip Top-Bottom", tag="tb")
    dpg.add_button(label="Reset Transform", tag="reset", callback=reset_img)


def create_widget_group():
    with dpg.child_window(
        pos=(dpg.get_viewport_width() - 300, 30),
        tag="widget_window",
        parent="widget_window_group",
    ):
        with dpg.group(label="Enhancer"):
            create_enhancer_group()
            dpg.add_separator()
        with dpg.group(label="Transform"):
            create_transform_group()
            dpg.add_separator()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


def main():
    dpg.create_context()
    dpg.create_viewport(title="Custom Title", resizable=True)
    dpg.set_viewport_resize_callback(callback=viewport_resize)
    with dpg.window(label="Photo Management", tag="photomanagement"):
        with dpg.menu_bar():
            d_id = choose_file(choose_file_callback)
            dpg.add_button(
                label="add file", callback=lambda: dpg.show_item(d_id)
            )
        # Image Window
        with dpg.group(horizontal=True, tag="widget_window_tag"):
            with dpg.child_window(
                pos=(10, 30), tag="img_window", horizontal_scrollbar=True
            ):
                dpg.add_text(default_value="Path ", tag="img_path")
        # Widget window
        with dpg.group(horizontal=True, tag="widget_window_group"):
            create_widget_group()

    dpg.setup_dearpygui()
    dpg.set_primary_window("photomanagement", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


main()
