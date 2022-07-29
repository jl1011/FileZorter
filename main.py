"""An app that allows you to sort your files visually."""

import os
import shutil

from dearpygui.dearpygui import *

current_directory = ""
dir_moved_to = []
dir_moved_from = []


def update_files_in_list() -> None:
    """Refreshes the file box at the bottom of the screen."""
    list_of_files = [f for f in os.listdir(get_value("directory"))]
    configure_item("files listbox", items=list_of_files)
    change_file_to_selected()


def connect() -> None:
    """Connects to the directory the user picked."""
    if get_value("directory") == "":
        set_value("log", "select a directory first!")
    elif get_value("status text") in ["UNCONNECTED", "FAILED", "CONNECTED"]:
        if os.path.exists(get_value("directory")):
            set_value("status text", "CONNECTED")
            configure_item("status text", color=(0, 255, 0))
            set_value("log", "Success.")
            update_files_in_list()
            configure_item("current file name text", color=(255, 255, 255))
            change_file_to_selected()
            update_files()
        else:
            set_value("status text", "FAILED")
            configure_item("status text", color=(255, 0, 0))
            set_value("log", "Oh no!   Are you sure the directory exists?")


def update_files() -> None:
    """Ensures the files are created in the directory."""
    for i in range(9):
        if i != 5:
            if get_value("box " + str(i)) is not None:
                path = get_value("directory") + "/" + str(get_value("box " + str(i)))
                if not os.path.exists(path):
                    os.mkdir(path)


def change_file_to_selected() -> None:
    """The file name in the center becomes the file selected in the listbox."""
    set_value("current file name text", get_value("files listbox"))


def move_to_num(number: str) -> None:
    """Moves the file in the center of the circle into whatever number was pressed."""
    box_text = get_value("box " + str(number))
    if box_text != "":
        filename = get_value("current file name text")
        common_dir = get_value("directory")
        if common_dir[-1] != "/":
            common_dir += "/"
        old_dir = common_dir + filename  # this doesn't need a slash because it's not always a folder
        dir_moved_from.append(common_dir)
        new_dir = common_dir + box_text
        if new_dir[-1] != "/":
            new_dir += "/"
        dir_moved_to.append(new_dir + filename)
        shutil.move(old_dir, new_dir)


def undo_movement() -> None:
    """Moves the file back to where it was before."""
    try:
        shutil.move(dir_moved_to.pop(), dir_moved_from.pop())
    except:
        raise Exception()


def key_down() -> None:
    """Handles the switching depending on the button pressed down."""
    for index, key in enumerate([mvKey_0, mvKey_1, mvKey_2, mvKey_3, mvKey_4, mvKey_5,
                                 mvKey_6, mvKey_7, mvKey_8, mvKey_9]):
        if is_key_pressed(key):
            try:
                move_to_num(str(index))
                update_files_in_list()
                try:
                    set_value("files listbox", index)
                    print("e")
                except:
                    set_value("files listbox", 0)
                    print("f")
            except:
                pass
        if is_key_pressed(mvKey_Z):
            undo_movement()
            update_files_in_list()


create_context()
setup_dearpygui()
create_viewport(title="FileZorter v0.0.0")
show_viewport()
with window(tag="bg"):
    add_text("current directory:", pos=(10, 20))
    add_input_text(tag="directory", hint="None", pos=(160, 20), width=500)
    # set_value("directory", "PUT YOUR MOST COMMON DIR HERE IF YOU'D LIKE, OTHERWISE YOU HAVE TO ENTER IT EVERY TIME")
    add_button(label="connect", pos=(160, 50), callback=connect)
    add_text("status:", tag="status text1", pos=(10, 50))
    add_text("UNCONNECTED", tag="status text", pos=(70, 50), color=(255, 0, 0))
    add_text("Enter a directory and hit connect!", tag="log", pos=(230, 50))
    with table(header_row=False, width=600):
        add_table_column(width_stretch=True, width=300)
        add_table_column()
        add_table_column()
        add_table_column()
        add_table_column(width_stretch=True, width=300)
        add_table_row()
        for i in range(4):
            with table_row():
                add_text()
                add_text()
                add_text()
                add_text()
        with table_row():
            add_text()
            add_input_text(indent=35, tag="box 7")
            add_input_text(indent=15, tag="box 8")
            add_input_text(tag="box 9")
        with table_row():
            add_text()
            add_text(default_value="(7)", indent=35)
            add_text(default_value="(8)", indent=15)
            add_text(default_value="(9)")
        with table_row():
            add_text()
            add_text()
            add_text()
        with table_row():
            add_text()
            add_input_text(tag="box 4")
            add_text("UNCONNECTED", tag="current file name text", color=(255, 0, 0))
            add_input_text(indent=35, tag="box 6")
        with table_row():
            add_text()
            add_text(default_value="(4)", indent=35, tag="")
            add_text()
            add_text(default_value="(6)", indent=35, tag="")
        with table_row():
            add_text()
            add_text()
            add_text()
        with table_row():
            add_text()
            add_input_text(indent=35, tag="box 1")
            add_input_text(indent=15, tag="box 2")
            add_input_text(tag="box 3")
        with table_row():
            add_text()
            add_text(default_value="(1)", indent=35)
            add_text(default_value="(2)", indent=15)
            add_text(default_value="(3)")
add_listbox(tag="files listbox", parent="bg", num_items=30, callback=change_file_to_selected)
set_primary_window("bg", True)
with handler_registry():
    add_key_down_handler(callback=key_down)
current_frame = 0
while is_dearpygui_running():
    current_frame += 1
    render_dearpygui_frame()
