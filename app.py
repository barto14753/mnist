import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk


# Globals
BUTTON_SIZE = 20
ROWS = 28
COLUMNS = 28
WIDTH = 900
HEIGHT = BUTTON_SIZE * ROWS

# Window
window = tk.Tk()
window.title("Mnist")

# Set the width and height of the window
def resize_window():
    window_width = WIDTH
    window_height = HEIGHT
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

BOARD = []

def get_button(x, y):
    row = y // BUTTON_SIZE
    column = x // BUTTON_SIZE
    return BOARD[row][column]

def on_left_click(event):
    x = window.winfo_pointerx() - window.winfo_rootx()
    y = window.winfo_pointery() - window.winfo_rooty()
    print("Mouse clicked at position:", x, y)
    button = get_button(x, y)
    button.config(bg="blue")

def on_right_click(event):
    x = window.winfo_pointerx() - window.winfo_rootx()
    y = window.winfo_pointery() - window.winfo_rooty()
    print("Mouse clicked at position:", x, y)
    button = get_button(x, y)
    button.config(bg="green")

def create_board():
    for i in range(ROWS):
        row = []
        for j in range(COLUMNS):
            button = tk.Frame(window, bg="green")
            button.config(width=BUTTON_SIZE, height=BUTTON_SIZE)
            button.grid(row=i, column=j)
            button.bind("<Button-1>", on_left_click)
            button.bind("<Button-3>", on_right_click)
            button.bind("<ButtonPress-1>", on_left_click)
            button.bind("<ButtonPress-3>", on_right_click)
            button.bind("<B1-Motion>", on_left_click)
            button.bind("<B3-Motion>", on_right_click)
            row.append(button)
        BOARD.append(row)

def create_buttons():
    custom_font = tkfont.Font(family="Arial", size=16)
    custom_large_font = tkfont.Font(family="Arial", size=36)

    title_label = tk.Label(window, text ="Mnist", font=custom_large_font)
    title_label.place(x=675, y=25)

    recognize_button = tk.Button(window, text ="RECOGNIZE", bg="green", font=custom_font)
    recognize_button.config(width=12)
    recognize_button.place(x=650, y=100)

    clear_button = tk.Button(window, text ="CLEAR", bg="red", font=custom_font)
    clear_button.config(width=12)
    clear_button.place(x=650, y=150)

    result_label = tk.Label(window, text ="Result: ", font=custom_font)
    result_label.place(x=650, y=225)

def main():
    window.resizable(False, False)
    resize_window()
    create_board()
    create_buttons()
    window.mainloop()

if __name__ == "__main__":
    main()