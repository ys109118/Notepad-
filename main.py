from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import simpledialog
from tkinter.colorchooser import askcolor
from tkinter.font import Font
import os

# Global variables
file = None
current_theme = "light"  # Default theme is light now
default_font_size = 14
font_size = default_font_size
suggestions = [
    "This is a suggestion.",
    "You can add more text here.",
    "Here is another suggested line.",
    "Feel free to use these suggestions.",
    "Auto-completion can help speed up your writing process.",
    "This is an example of a longer paragraph suggestion. You can use this to quickly add multiple lines of text at once.",
    "Explore new ideas and thoughts.",
    "Writing is a journey of self-expression.",
    "Let your creativity flow.",
    "Use the power of words to inspire.",
    "Captivate your audience with compelling content.",
    "Every word counts in crafting your message.",
    "Writing can illuminate even the darkest corners of the mind.",
    "Words have the power to change perspectives.",
    "Embrace the art of storytelling.",
    "Convey your emotions through your writing.",
    "Discover new ways to articulate your thoughts.",
    "Challenge yourself to write something unconventional.",
    "Seek inspiration from everyday experiences.",
    "Write with passion and purpose."
]

# Function to toggle between light and dark themes
def toggle_theme():
    update_theme()
    update_status_bar()

# Function to open a file
def open_file(event=None):
    global file
    file = fd.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ("Text File", "*.txt*")])

    if file != '':
        root.title(f"{os.path.basename(file)} - Cool Futuristic Notepad")
        text_area.delete(1.0, END)
        with open(file, "r") as file_:
            text_area.insert(1.0, file_.read())
        mb.showinfo("File Opened", f"Opened: {os.path.basename(file)}")
    else:
        file = None

# Function to open a new file
def open_new_file(event=None):
    global file
    file = None
    root.title("Untitled - Cool Futuristic Notepad")
    text_area.delete(1.0, END)
    mb.showinfo("New File", "New file created.")

# Function to save a file
def save_file(event=None):
    global file
    if file is None:
        file = fd.asksaveasfilename(initialfile='Untitled.txt', defaultextension='.txt',
                                    filetypes=[("Text File", "*.txt*"), ("All Files", "*.*")])
    if file != '':
        with open(file, "w") as file_:
            file_.write(text_area.get(1.0, END))
        root.title(f"{os.path.basename(file)} - Cool Futuristic Notepad")
        mb.showinfo("File Saved", f"Saved: {os.path.basename(file)}")

# Function to handle exiting the application
def exit_application(event=None):
    if mb.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()

# Function to copy text
def copy_text(event=None):
    text_area.event_generate("<<Copy>>")

# Function to cut text
def cut_text(event=None):
    text_area.event_generate("<<Cut>>")

# Function to paste text:
def paste_text(event=None):
    text_area.event_generate("<<Paste>>")

# Function to select all text
def select_all(event=None):
    text_area.tag_add('sel', '1.0', 'end')

# Function to delete the last character
def delete_last_char(event=None):
    text_area.event_generate("<<KeyPress-Delete>>")

# Function to display about information
def about_notepad():
    mb.showinfo("About Cool Futuristic Notepad", "This is just another Notepad, but this is better than all others")

# Function to display all available commands
def about_commands():
    commands = """
Under the File Menu:
- 'New' clears the entire Text Area
- 'Open File' clears text and opens another file
- 'Save As' saves your current file
- 'Exit' closes the application

Under the Edit Menu:
- 'Copy' copies the selected text to your clipboard
- 'Cut' cuts the selected text and removes it from the text area
- 'Paste' pastes the copied/cut text
- 'Delete' deletes the last character
- 'Select All' selects the entire text
- 'Find' allows finding text within the document
- 'Go To' allows jumping to a specific line number

Under the Format Menu:
- 'Change Font Color' allows changing the font color
- 'Change Font' allows changing the font family

Under the View Menu:
- 'Zoom In', 'Zoom Out', 'Reset Zoom' adjust text size
- 'Toggle Theme' switches between light and dark themes

Under the Help Menu:
- 'About Cool Futuristic Notepad' displays general information about the application
- 'Update Logs' shows recent updates and changes
"""
    mb.showinfo(title="All commands", message=commands)

# Function to count words in the text area
def count_words():
    content = text_area.get(1.0, END)
    words = content.split()
    return len(words)

# Function to find text
def find_text():
    find_str = simpledialog.askstring("Find", "Enter text to find:")
    if find_str:
        text_area.tag_remove('found', '1.0', END)
        start_pos = '1.0'
        while True:
            start_pos = text_area.search(find_str, start_pos, stopindex=END, nocase=1)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(find_str)}c"
            text_area.tag_add('found', start_pos, end_pos)
            start_pos = end_pos
        text_area.tag_config('found', foreground='white', background='blue')

        # Bind a function to remove 'found' tags on click
        text_area.bind("<Button-1>", remove_found_tag)

# Function to go to line
def go_to_line():
    try:
        max_line_number = int(text_area.index(END).split('.')[0])
        line_num = simpledialog.askinteger("Go To", "Enter line number:", initialvalue=1, minvalue=1, maxvalue=max_line_number)
        if line_num:
            line_pos = f"{line_num}.0"
            text_area.mark_set("insert", line_pos)
            text_area.see("insert")
            text_area.focus_set()
            mb.showinfo("Go To Line", f"Moved cursor to line {line_num}.")
    except ValueError:
        pass  # Handle invalid input gracefully

# Function to show update logs
def show_update_logs():
    update_log = """
    Update Logs:
    ---------------------
    Version 1.3.0:
    - Added 'Change Font' functionality to allow changing the font family.

    Version 1.2.0:
    - Added 'Change Font Color' functionality with color picker.

    Version 1.1.0:
    - Added 'Find' functionality to search within the document.
    - Implemented 'Go To' feature for jumping to specific line numbers.

    Version 1.0.0:
    - Initial release of Cool Futuristic Notepad.
    """
    mb.showinfo("Update Logs", update_log)

# Function to suggest lines and paragraphs
def suggest_text(event):
    current_text = text_area.get("insert linestart", "insert")
    if current_text and event.char in (' ', '.'):
        for suggestion in suggestions:
            if suggestion.startswith(current_text):
                text_area.insert("insert", suggestion[len(current_text):])
                return "break"
    return None

# Functions to zoom in, zoom out, and reset zoom
def zoom_in(event=None):
    global font_size
    font_size += 2
    text_area.config(font=("Segoe UI", font_size))

def zoom_out(event=None):
    global font_size
    font_size -= 2
    text_area.config(font=("Segoe UI", font_size))

def reset_zoom(event=None):
    global font_size
    font_size = default_font_size
    text_area.config(font=("Segoe UI", font_size))

# Function to change text alignment
def align_text(alignment):
    text_area.tag_configure("align", justify=alignment)
    text_area.tag_add("align", "sel.first", "sel.last")

# Function to update status bar with word and character count
def update_status_bar(event=None):
    word_count = count_words()
    char_count = len(text_area.get(1.0, END)) - 1  # exclude newline at end
    status_text = f"Words: {word_count} | Characters: {char_count}"
    status_bar.config(text=status_text)

# Function to update the theme
def update_theme():
    global current_theme
    if current_theme == "light":
        root.config(bg='#2b2b2b')
        text_area.config(fg='white', bg='#2b2b2b', insertbackground='white', font=("Segoe UI", font_size))
        status_bar.config(bg='#e0e0e0', fg='black')
        menu_bar.config(bg='#e0e0e0', fg='black')
        scrollbar.config(bg='#e0e0e0', troughcolor='#f0f0f0')
        current_theme = "dark"
    else:
        root.config(bg='#ffffff')
        text_area.config(fg='black', bg='#ffffff', insertbackground='black', font=("Segoe UI", font_size))
        status_bar.config(bg='#e0e0e0', fg='black')
        menu_bar.config(bg='#e0e0e0', fg='black')
        scrollbar.config(bg='#e0e0e0', troughcolor='#f0f0f0')
        current_theme = "light"

# Function to remove 'found' tags from text_area
def remove_found_tag(event):
    text_area.tag_remove('found', '1.0', END)

# Function to ask for font color using color chooser
def ask_color():
    color = askcolor(title="Choose Font Color")[1]
    if color:
        text_area.config(foreground=color)

# Function to change font family
def change_font():
    font_name = simpledialog.askstring("Font", "Enter Font Name")
    if font_name:
        global font_size
        text_area.config(font=(font_name, font_size))

# Initialize the GUI
root = Tk()
root.title("Untitled - Cool Futuristic Notepad")
root.geometry("800x600")

# Creating a Menu Bar
menu_bar = Menu(root)

# File Menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=open_new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_application, accelerator="Alt+F4")
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut_text, accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=copy_text, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste_text, accelerator="Ctrl+V")
edit_menu.add_command(label="Delete", command=delete_last_char, accelerator="Del")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find_text, accelerator="Ctrl+F")
edit_menu.add_command(label="Go To", command=go_to_line, accelerator="Ctrl+G")
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Format Menu
format_menu = Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Change Font Color", command=ask_color)
format_menu.add_command(label="Change Font", command=change_font)
menu_bar.add_cascade(label="Format", menu=format_menu)

# View Menu
view_menu = Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Zoom In", command=zoom_in, accelerator="Ctrl++")
view_menu.add_command(label="Zoom Out", command=zoom_out, accelerator="Ctrl+-")
view_menu.add_command(label="Reset Zoom", command=reset_zoom, accelerator="Ctrl+0")
view_menu.add_separator()
view_menu.add_command(label="Toggle Theme", command=toggle_theme)
menu_bar.add_cascade(label="View", menu=view_menu)

# Help Menu
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=about_notepad)
help_menu.add_command(label="Commands", command=about_commands)
help_menu.add_command(label="Update Logs", command=show_update_logs)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Adding Menu Bar to root
root.config(menu=menu_bar)

# Creating a Scrollbar
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

# Creating a Text Area
text_area = Text(root, wrap=WORD, yscrollcommand=scrollbar.set, undo=True)
text_area.pack(fill=BOTH, expand=1)

# Configuring the Scrollbar
scrollbar.config(command=text_area.yview)

# Status Bar
status_bar = Label(root, text='Words: 0 | Characters: 0', bd=1, relief=SUNKEN, anchor=W)
status_bar.pack(side=BOTTOM, fill=X)

# Event bindings
root.bind("<Control-n>", open_new_file)
root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Alt-F4>", exit_application)
root.bind("<Control-x>", cut_text)
root.bind("<Control-c>", copy_text)
root.bind("<Control-v>", paste_text)
root.bind("<Delete>", delete_last_char)
root.bind("<Control-a>", select_all)
root.bind("<Control-f>", find_text)
root.bind("<Control-g>", go_to_line)
root.bind("<Control-plus>", zoom_in)
root.bind("<Control-minus>", zoom_out)
root.bind("<Control-0>", reset_zoom)
text_area.bind("<KeyRelease>", update_status_bar)

# Start the GUI
root.mainloop()
