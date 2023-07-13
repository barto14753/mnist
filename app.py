import tkinter as tk
import tkinter.font as tkfont
import torch
import torch.nn.functional as F
from model import Net

# globals
BUTTON_SIZE = 20
ROWS = 28
COLUMNS = 28
WIDTH = 900
HEIGHT = BUTTON_SIZE * ROWS

# window
window = tk.Tk()
window.title("Mnist")

# state
state = {}

# theme
BUTTON_COLOR = "blue"
BG_COLOR = "white"

# model
gpu = torch.device("cuda")
model_state = torch.load("mnist_cnn.pt", map_location=torch.device('cuda'))
model = Net()
model.load_state_dict(model_state)


# set the width and height of the window
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
    if x < 0 or y < 0:
        return
    button = get_button(x, y)
    button.config(bg=BUTTON_COLOR)
    show_prediction()


def on_right_click(event):
    x = window.winfo_pointerx() - window.winfo_rootx()
    y = window.winfo_pointery() - window.winfo_rooty()
    if x < 0 or y < 0:
        return
    button = get_button(x, y)
    button.config(bg=BG_COLOR)
    show_prediction()


def clear():
    for row in BOARD:
        for button in row:
            button.config(bg=BG_COLOR)
    state["result_label"].config(text="")


def show_prediction():
    tensor = []
    for row in BOARD:
        r = []
        for button in row:
            bit = 0.0 if button.cget("background") == BG_COLOR else 1.0
            r.append(bit)
        tensor.append(r)
    tensor = torch.Tensor([[tensor]])
    prediction = predict(tensor)
    state["result_label"].config(text=str(prediction))


def predict(tensor):
    result_tensor = model(tensor)
    probabilities = F.softmax(result_tensor, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1)
    return predicted_class[0].item()


def create_board():
    for i in range(ROWS):
        row = []
        for j in range(COLUMNS):
            button = tk.Frame(window, bg=BG_COLOR)
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
    custom_huge_font = tkfont.Font(family="Arial", size=64)

    title_label = tk.Label(window, text="Mnist", font=custom_large_font)
    title_label.place(x=675, y=25)
    clear_button = tk.Button(window, text="CLEAR", bg="red", font=custom_font, command=clear)
    clear_button.config(width=12)
    clear_button.place(x=650, y=150)
    prediction_label = tk.Label(window, text="Prediction", font=custom_font)
    prediction_label.place(x=685, y=225)
    result_label = tk.Label(window, text="", font=custom_huge_font)
    result_label.place(x=710, y=250)
    state["result_label"] = result_label


def main():
    window.resizable(False, False)
    resize_window()
    create_board()
    create_buttons()
    window.mainloop()


if __name__ == "__main__":
    main()
