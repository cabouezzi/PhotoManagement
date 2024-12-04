import dearpygui.dearpygui as dpg

# from edit import ImageTransform

dpg.create_context()

pos = []


def drag_callback(sender, app_data):
    pos.append(dpg.get_mouse_pos())


def release_callback(sender, app_data):
    print(f"start {pos[2]}, stop {pos[-1]}")
    dpg.draw_rectangle(
        pos[2], pos[-1], parent="main_window", tag="crop_window"
    )


width, height, channels, data = dpg.load_image(
    "C:\\Users\\lemin\\PhotoManagement\\photomanagement\\tests\\photos\\international.jpg"
)

with dpg.texture_registry(show=True):
    dpg.add_static_texture(
        width=width, height=height, default_value=data, tag="texture_tag"
    )
with dpg.handler_registry():
    dpg.add_mouse_drag_handler(callback=drag_callback)
    dpg.add_mouse_release_handler(callback=release_callback)

with dpg.window(label="Tutorial", tag="main_window"):
    dpg.add_text("some text", tag="text")
    print(dpg.get_value("text"))
    dpg.add_image("texture_tag", tag="img")
    pos = dpg.get_item_pos("img")
    size = (dpg.get_item_width("img"), dpg.get_item_height("img"))


dpg.create_viewport(title="Custom Title", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
# from edit import ImageEnhancer
# import numpy as np

# obj = ImageEnhancer(
#     "C:\\Users\\lemin\\PhotoManagement\\photomanagement\\tests\\photos\\in-the-lab.jpg"
# )

# new_img = obj.brighten(0.39)
# # new_img = obj.sharpen(0.3)
# # new_img = obj.contrast(0.3)
# # new_img = obj.colorize(0.3)
# new_arr = np.array(new_img.getdata(), dtype=np.uint8) / 255
# print(new_arr[:20])
# new_img.show()

# obj = ImageTransform(
#     "C:\\Users\\lemin\\PhotoManagement\\photomanagement\\tests\\photos\\international.jpg"
# )
# new_img = obj.crop([24.0, 19.0, 186.0, 323.0])
# new_img.show()
