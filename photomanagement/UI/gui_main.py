import dearpygui.dearpygui as dpg
from gui_cv import edit_main
from edit_cv import HandleImageDPG

"""
File Handler
"""


def load_image(path):
    try:
        # when there is path
        if dpg.get_value("img_path") != "Path ":
            print("img already exist")
            # width, height, channels, data = dpg.load_image(path)
            dpg.delete_item("texture_tag")
            dpg.remove_alias("texture_tag")
            dpg.delete_item("texture_registry")
            dpg.delete_item("image_tag")
        with dpg.texture_registry(show=False, tag="texture_registry"):
            handle_img_obj = HandleImageDPG()
            rgba_img = handle_img_obj.cv2_open_img(path)
            cv2_data = handle_img_obj.texture_to_data(rgba_img)
            dpg.add_static_texture(
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
        dpg.set_item_callback("apply_btn", handle_img_obj.update_texture)
        # create_widget_group(handle_img_obj)
        return handle_img_obj
    except ValueError:
        print("cannot load file. path does not exist")


def choose_img_callback(sender, app_data):
    """
    Load image, adjust image path text, load widget groups
    """
    path = app_data["file_path_name"]
    if dpg.does_item_exist("photo_window"):
        if not dpg.get_item_state("photo_window")["toggled_open"]:
            cancel_img_callback()
    edit_main()
    load_image(path)


def cancel_img_callback():
    dpg.delete_item("widget_handler")
    dpg.remove_alias("widget_handler")
    dpg.delete_item("photo_window")
    dpg.delete_item("texture_registry")


def main():
    file_extensions = ["jpeg", "jpg", "png", "webp", "heic"]
    dpg.create_context()
    dpg.create_viewport(title="Photo Management", resizable=True)
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=choose_img_callback,
        cancel_callback=cancel_img_callback,
        id="image_dialog",
        width=700,
        height=400,
    ):
        for file_extension in file_extensions:
            dpg.add_file_extension(
                f".{file_extension}", color=(150, 255, 150, 255)
            )
    dpg.add_file_dialog(
        directory_selector=True,
        show=False,
        id="dir_dialog",
        width=700,
        height=400,
    )
    with dpg.window(
        label="Directory",
        tag="main_window",
        width=dpg.get_viewport_width(),
        height=dpg.get_viewport_height(),
    ):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_button(
                    label="Edit Image ...",
                    callback=lambda: dpg.show_item("image_dialog"),
                )
                dpg.add_button(label="Open Photo Directory ...")
    # dpg.set_primary_window("photo_window", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


main()
