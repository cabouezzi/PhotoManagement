import dearpygui.dearpygui as dpg
from gui_cv import choose_img_callback, cancel_img_callback
from PIL import Image
import glob
import DearPyGui_ImageController as dpg_img
from photomanagement import Database, Speech
import pathlib

"""
PIL images to dpg images
"""
db = None
speech = None
# home_dir = pathlib.Path.home() / ".photomanagement"
home_dir = "C:\\Users\\Owen\\code_anh\\PhotoManagement\\db"


def img_to_1D_arr(image):
    img_1D_arr = []
    image_data = image.getdata()
    if image_data.bands == 3:
        for pixel in image_data:
            img_1D_arr.extend(
                (pixel[0] / 255, pixel[1] / 255, pixel[2] / 255, 1)
            )
    else:
        for pixel in image_data:
            img_1D_arr.extend(
                (
                    pixel[0] / 255,
                    pixel[1] / 255,
                    pixel[2] / 255,
                    pixel[3] / 255,
                )
            )
    del image_data
    return img_1D_arr


# def image_to_dpg_texture(image, texture_registry):
#     rgba_image = image.convert("RGBA")
#     img_1d_array = img_to_1D_arr(rgba_image)
#     dpg_texture_tag = dpg.add_static_texture(
#         width=rgba_image.width,
#         height=rgba_image.height,
#         default_value=img_1d_array,
#         parent=texture_registry,
#     )

#     rgba_image.close()
#     del img_1d_array, rgba_image
#     return dpg_texture_tag


"""
File Handler
"""


def speak(sender, app_data, user_data):
    desc = speech.speak(user_data)
    db.update_photo(user_data, desc)
    print(desc)


# def print_userdata(_, _, user_data):
#     # print(f"sender {sender}")
#     # print(f"app_data {app_data}")
#     # print(f"user_data {user_data}")
#     if len(dpg.get_item_children("info_window")) > 0:
#         dpg.delete_item("info_window", children_only=True)
#     p = user_data
#     with dpg.texture_registry():
#         im_1D = img_to_1D_arr(p.data.convert("RGBA"))
#         texture_tag = dpg.add_static_texture(
#             width=p.data.width,
#             height=p.data.height,
#             default_value=im_1D,
#         )
#         dpg.add_image(texture_tag, parent="info_window")
#         with dpg.group(parent="info_window"):
#             dpg.add_text(f"Id: {p.id}")
#             dpg.add_text(f"Title: {p.title}")
#             dpg.add_text(f"Time Created: {p.time_created}")
#             dpg.add_text(f"Time Last Modified: {p.time_last_modified}")
def delete_img(sender, app_data, user_data):
    db.delete_images(user_data["photo"])
    dpg.delete_item(user_data["tag"])
    dpg.delete_item(user_data["sender"])
    dpg.delete_item("info_window", children_only=True)


def find_duplicates(sender, app_data, user_data):
    p = user_data
    resulted_photos = db.query_with_photo(photo=p)
    with dpg.window(label="Results", width=500, height=500) as res:
        with dpg.texture_registry():
            for res_photo in resulted_photos:
                im_1D = img_to_1D_arr(res_photo.data.convert("RGBA"))
                texture_tag = dpg.add_static_texture(
                    width=res_photo.data.width,
                    height=res_photo.data.height,
                    default_value=im_1D,
                )
                img_tag = dpg.add_image_button(
                    texture_tag,
                    parent=res,
                    callback=extra_fn,
                    user_data=res_photo,
                )


def find_identical(sender, app_data, user_data):
    p = user_data
    resulted_photos = db.scan_duplicates_for_photo(photo=p)
    with dpg.window(label="Results", width=500, height=500) as res:
        with dpg.texture_registry():
            for res_photo in resulted_photos:
                im_1D = img_to_1D_arr(res_photo.data.convert("RGBA"))
                texture_tag = dpg.add_static_texture(
                    width=res_photo.data.width,
                    height=res_photo.data.height,
                    default_value=im_1D,
                )
                img_tag = dpg.add_image_button(
                    texture_tag,
                    parent=res,
                    callback=extra_fn,
                    user_data=res_photo,
                )


def extra_fn(sender, app_data, user_data):
    if len(dpg.get_item_children("info_window")) > 0:
        dpg.delete_item("info_window", children_only=True)
    p = user_data
    with dpg.texture_registry():
        im_1D = img_to_1D_arr(p.data.convert("RGBA"))
        texture_tag = dpg.add_static_texture(
            width=p.data.width,
            height=p.data.height,
            default_value=im_1D,
        )
        img_tag = dpg.add_image(texture_tag, parent="info_window")
        with dpg.group(parent="info_window"):
            dpg.add_text(f"Id: {p.id}")
            dpg.add_text(f"Title: {p.title}")
            dpg.add_text(f"Time Created: {p.time_created}")
            dpg.add_text(f"Time Last Modified: {p.time_last_modified}")
    photo = user_data
    with dpg.group(parent="info_window", horizontal=True):
        dpg.add_separator()
        dpg.add_button(
            label="Edit",
            user_data=photo.data.filename,
            callback=choose_img_callback,
        )
        dpg.add_button(
            label="Find Duplicates",
            callback=find_duplicates,
            user_data=photo,
        )
        dpg.add_button(
            label="Find Identical",
            callback=find_identical,
            user_data=photo,
        )
    with dpg.group(parent="info_window", horizontal=True):
        dpg.add_button(label="Speak", callback=speak, user_data=photo)
        dpg.add_button(
            label="Delete",
            callback=delete_img,
            user_data={"photo": photo, "tag": img_tag, "sender": sender},
        )


def search_photo(sender, app_data):
    # with dpg.item_handler_registry() as search_handler_reg:
    #     dpg.add_item_double_clicked_handler(callback=print_userdata)
    resulted_photos = db.query_with_text(app_data)
    with dpg.window(label="Results", width=500, height=500) as res:
        with dpg.texture_registry():
            for res_photo in resulted_photos:
                im_1D = img_to_1D_arr(res_photo.data.convert("RGBA"))
                texture_tag = dpg.add_static_texture(
                    width=res_photo.data.width,
                    height=res_photo.data.height,
                    default_value=im_1D,
                )
                img_tag = dpg.add_image_button(
                    texture_tag,
                    parent=res,
                    callback=extra_fn,
                    user_data=res_photo,
                )
                # dpg.bind_item_handler_registry(
                #     img_tag, search_handler_reg
                # )


def choose_dir_callback(sender, app_data):
    dir_path = app_data["file_path_name"]
    load_all_img(path=dir_path)
    # db = Database(dir_path)
    # print(app_data)


def load_all_img(path):
    db.add_images_from_directory(path)
    photos = db.query_with_text("hi")
    with dpg.texture_registry() as text_reg:
        for photo in photos:
            im_1D = img_to_1D_arr(photo.data.convert("RGBA"))
            texture_tag = dpg.add_static_texture(
                width=photo.data.width,
                height=photo.data.height,
                default_value=im_1D,
            )
            img_tag = dpg.add_image_button(
                texture_tag,
                parent="image_group",
                callback=extra_fn,
                user_data=photo,
            )
            # with dpg.popup(img_tag):
            #     dpg.add_button(label="Find Duplicates")
            #     dpg.add_button(
            #         label="Edit",
            #         user_data=photo.data.filename,
            #         callback=choose_img_callback,
            #     )
            #     dpg.add_button(label="Speak", user_data=photo)
            #     dpg.add_button(label="Delete")
    dpg.set_item_callback("search_box", callback=search_photo)


"""
Create layout
"""


"""
Window Display and Resize Configuration
"""


def viewport_resize(sender, app_data):
    dpg.configure_item(
        "main_window",
        width=dpg.get_viewport_width(),
        height=dpg.get_viewport_height(),
    )


def main():
    file_extensions = ["jpeg", "jpg", "png"]
    global db, speech
    db = Database(home_dir)
    speech = Speech()
    dpg.create_context()
    dpg.create_viewport(title="Photo Management", resizable=True)
    dpg.set_viewport_resize_callback(callback=viewport_resize)
    with dpg.item_handler_registry(tag="info_window_handler"):
        dpg.add_item_resize_handler(
            callback=lambda: dpg.set_item_pos(
                "info_window",
                pos=(dpg.get_item_width("main_window") - 400, 30),
            )
        )
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=choose_img_callback,
        cancel_callback=cancel_img_callback,
        tag="image_dialog",
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
        tag="dir_dialog",
        width=700,
        height=400,
        callback=choose_dir_callback,
    )
    with dpg.window(
        label="Directory",
        tag="main_window",
        width=dpg.get_viewport_width(),
        height=dpg.get_viewport_height(),
    ):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                # dpg.add_button(
                #     label="Edit Image ...",
                #     callback=lambda: dpg.show_item("image_dialog"),
                # )
                dpg.add_button(
                    label="Open Photo Directory ...",
                    callback=lambda: dpg.show_item("dir_dialog"),
                )
            dpg.add_button(label="Find Duplicates", tag="dup_btn")
        with dpg.group(horizontal=True):
            with dpg.child_window(
                pos=(10, 30), tag="all_img_window", horizontal_scrollbar=True
            ):
                dpg.add_input_text(
                    label="Search", width=500, tag="search_box", on_enter=True
                )
                with dpg.group(tag="image_group"):
                    pass
        with dpg.group(horizontal=True, tag="info_window_group"):
            dpg.add_child_window(
                pos=(dpg.get_viewport_width() - 400, 30),
                tag="info_window",
                parent="info_window_group",
                width=400,
                horizontal_scrollbar=True,
            )
    dpg.set_primary_window("main_window", True)
    dpg.bind_item_handler_registry("main_window", "info_window_handler")
    dpg.set_global_font_scale(1.5)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


main()
