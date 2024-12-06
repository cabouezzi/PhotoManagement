import dearpygui.dearpygui as dpg
from edit_cv import HandleImageDPG

"""
Variables
"""


"""
File Handler
"""


def load_img_init(path):
    try:
        # when there is path
        if dpg.get_value("img_path") != "Path ":
            # width, height, channels, data = dpg.load_image(path)
            dpg.delete_item("texture_tag")
            dpg.remove_alias("texture_tag")
            dpg.delete_item("image_tag")
        with dpg.texture_registry(show=True, tag="texture_registry"):
            handle_img_obj = HandleImageDPG()
            rgba_img = handle_img_obj.cv2_open_img(path=path)
            cv2_data = handle_img_obj.texture_to_data(rgba_img)
            dpg.add_raw_texture(
                width=rgba_img.shape[1],
                height=rgba_img.shape[0],
                default_value=cv2_data,
                tag="texture_tag",
            )
            dpg.add_image(
                "texture_tag",
                parent="img_window",
                tag="image_tag",
            )
            dpg.set_value("img_path", value=f"Path {path}")
            create_widget_group(handle_img_obj)
    except ValueError:
        print("cannot load file. path does not exist")


def choose_file_callback(sender, app_data):
    """
    Load image, adjust image path text, load widget groups
    """
    path = app_data["file_path_name"]
    # width, height, channels, data = dpg.load_image(path)
    handle_img_obj = HandleImageDPG()
    rgba_img = handle_img_obj.cv2_open_img(path=path)
    cv2_data = handle_img_obj.texture_to_data(rgba_img)
    try:
        # when there is path
        if dpg.get_value("img_path") != "Path ":
            # width, height, channels, data = dpg.load_image(path)
            dpg.delete_item("texture_tag")
            dpg.remove_alias("texture_tag")
            dpg.delete_item("image_tag")
        with dpg.texture_registry(show=True, tag="texture_registry"):
            dpg.add_raw_texture(
                width=rgba_img.shape[1],
                height=rgba_img.shape[0],
                default_value=cv2_data,
                tag="texture_tag",
            )
            dpg.add_image(
                "texture_tag",
                parent="img_window",
                tag="image_tag",
            )
        dpg.set_value("img_path", value=f"Path {path}")
        create_widget_group(handle_img_obj)
    except ValueError:
        print("cannot load file. path does not exist")


"""
Widget loading and layout
"""


def create_widget_group(obj):
    with dpg.group(parent="widget_window"):
        dpg.add_text(default_value="Enhance")
        dpg.add_input_int(
            label="Brightness",
            default_value=0,
            tag="bri",
            step=1,
            step_fast=5,
            min_value=0,
            max_value=100,
        )
        dpg.add_input_double(
            label="Contrast",
            default_value=1,
            tag="con",
            step=0.1,
            min_value=0.1,
            max_value=5,
        )
        dpg.add_input_double(
            label="Hue",
            default_value=1,
            tag="hue",
            step=0.1,
            step_fast=2,
            min_value=-5,
            max_value=5,
        )
        dpg.add_input_double(
            label="Saturation",
            default_value=1,
            tag="sat",
            step=0.1,
            step_fast=2,
            min_value=0,
            max_value=10,
        )
        dpg.add_button(
            label="Apply Changes",
            callback=obj.update_texture,
            user_data="texture_tag",
        )


"""
Window Display and Resize Configuration
"""


def viewport_resize(sender, app_data):
    dpg.set_item_pos("widget_window", pos=(dpg.get_viewport_width() - 400, 30))


def main():
    file_extensions = ["jpeg", "jpg", "png", "webp", "heic"]
    dpg.create_context()
    dpg.create_viewport(title="Photo Management", resizable=True)
    dpg.set_viewport_resize_callback(callback=viewport_resize)
    with dpg.window(label="Main window", tag="main_window"):
        with dpg.menu_bar():
            with dpg.file_dialog(
                directory_selector=False,
                show=False,
                callback=choose_file_callback,
                id="file_dialog",
                width=700,
                height=400,
            ):
                for file_extension in file_extensions:
                    dpg.add_file_extension(
                        f".{file_extension}", color=(150, 255, 150, 255)
                    )
            dpg.add_button(
                label="add file", callback=lambda: dpg.show_item("file_dialog")
            )
        with dpg.group(horizontal=True):
            with dpg.child_window(
                pos=(10, 30), tag="img_window", horizontal_scrollbar=True
            ):
                dpg.add_text(default_value="Path ", tag="img_path")
        with dpg.group(horizontal=True, tag="widget_window_group"):
            dpg.add_child_window(
                pos=(dpg.get_viewport_width() - 400, 30),
                tag="widget_window",
                parent="widget_window_group",
            )
            dpg.add_text(
                default_value="Add a file to load widget",
                tag="info",
                parent="widget_window",
            )
    dpg.setup_dearpygui()
    dpg.set_primary_window("main_window", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


main()
