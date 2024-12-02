import dearpygui.dearpygui as dpg


# choose file
# --------------------------------------------------------------------------------------------------------------------------------------------------
def choose_file_callback(_, app_data):
    print(app_data)
    path = app_data["file_path_name"]
    print(path)
    # dpg.set_value("file_text", value=path)
    load_img(path)


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


def load_img(path):
    try:
        width, height, channels, data = dpg.load_image(path)
        with dpg.texture_registry(show=True):
            dpg.add_static_texture(
                width=width,
                height=height,
                default_value=data,
                tag="texture_tag",
            )
        dpg.add_image("texture_tag", parent="img_window")
    except ValueError:
        print("cannot load file. path does not exist")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Widget
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
def create_widget_group():
    with dpg.group(horizontal=True):
        with dpg.child_window(pos=(600, 30)):
            with dpg.group(label="Enhancer"):
                dpg.add_slider_double(label="Brightness", default_value=30)
                dpg.add_slider_double(label="Sharpness", default_value=30)
                dpg.add_slider_double(
                    label="Contrast",
                    clamped=True,
                    min_value=0.0,
                    max_value=1.0,
                )
                dpg.add_slider_double(
                    label="Contrast",
                    clamped=True,
                    min_value=0.0,
                    max_value=1.0,
                )


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


def main():
    dpg.create_context()
    d_id = choose_file(choose_file_callback, choose_file_cancel)
    with dpg.window(label="Photo Management", tag="photomanagement"):
        with dpg.menu_bar():
            dpg.add_button(
                label="add file", callback=lambda: dpg.show_item(d_id)
            )
            # dpg.add_text(
            #     tag="file_text",
            #     default_value="C:\\Users\\lemin\\PhotoManagement\\photomanagement\\tests\\photos\\international.jpg",
            # )
        with dpg.group(horizontal=True):
            with dpg.child_window(pos=(10, 30), tag="img_window"):
                dpg.add_text("Some text")
        create_widget_group()

    dpg.create_viewport(title="Custom Title", width=900, height=600)
    dpg.setup_dearpygui()
    dpg.set_primary_window("photomanagement", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


main()
