import dearpygui.dearpygui as dpg

dpg.create_context()

width, height, channels, data = dpg.load_image(
    "C:\\Users\\lemin\\OneDrive\\Documents\\Bursar\\international.jpg"
)

with dpg.texture_registry(show=True):
    dpg.add_static_texture(
        width=width, height=height, default_value=data, tag="texture_tag"
    )

with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag")
    dpg.add_button(label="Button 1")
    dpg.add_button(label="Button 2")
    with dpg.group():
        dpg.add_button(label="Button 3")
        dpg.add_button(label="Button 4")
        with dpg.group() as group1:
            pass
dpg.add_button(label="Button 6", parent=group1)
dpg.add_button(label="Button 5", parent=group1)


dpg.create_viewport(title="Custom Title", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
