# import dearpygui.dearpygui as dpg


# dpg.create_context()
# dpg.create_viewport(title="Custom Title", width=600, height=300)


# def slider_callback(sender, app_data):
#     print("Sender: ", sender)
#     print("App Data: ", app_data)


# with dpg.window(label="Example Window"):
#     dpg.add_text("Hello, world")
#     dpg.add_button(label="Save")
#     dpg.add_input_text(label="string", default_value="Quick brown fox")
#     dpg.add_slider_float(
#         label="float",
#         default_value=0.273,
#         max_value=1,
#         callback=slider_callback,
#         tag="some_slider",
#     )

# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()
from edit import ImageEnhancer
import numpy as np

obj = ImageEnhancer(
    "C:\\Users\\lemin\\PhotoManagement\\photomanagement\\tests\\photos\\in-the-lab.jpg"
)

new_img = obj.brighten(0.39)
# new_img = obj.sharpen(0.3)
# new_img = obj.contrast(0.3)
# new_img = obj.colorize(0.3)
new_arr = np.array(new_img.getdata(), dtype=np.uint8) / 255
print(new_arr[:20])
new_img.show()
