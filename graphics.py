from tkinter import Tk, BOTH, Canvas, Frame, Button, Label, Entry, StringVar

DARK_BACKGROUND = "#121212"
LIGHT_FOREGROUND = "#E0E0E0"
BUTTON_BACKGROUND = "#333333"
BUTTON_FOREGROUND = LIGHT_FOREGROUND
SOLVE_PATH_COLOR = "#00FFFF"
UNDO_PATH_COLOR = "#555555"


class Window:
    def __init__(self, width, height, default_rows, default_cols, default_cell_size):
        self.__root = Tk()
        self.__root.title("Maze Solver - Dark Mode")
        self.__root.configure(bg=DARK_BACKGROUND)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__param_frame = Frame(self.__root, bg=DARK_BACKGROUND)
        self.__param_frame.pack(fill="x", side="top", pady=5)

        Label(
            self.__param_frame, text="Rows:", bg=DARK_BACKGROUND, fg=LIGHT_FOREGROUND
        ).pack(side="left", padx=(10, 0))
        self.rows_var = StringVar(value=str(default_rows))
        Entry(
            self.__param_frame,
            textvariable=self.rows_var,
            width=5,
            bg=BUTTON_BACKGROUND,
            fg=BUTTON_FOREGROUND,
            relief="flat",
        ).pack(side="left", padx=(0, 10))

        Label(
            self.__param_frame, text="Cols:", bg=DARK_BACKGROUND, fg=LIGHT_FOREGROUND
        ).pack(side="left")
        self.cols_var = StringVar(value=str(default_cols))
        Entry(
            self.__param_frame,
            textvariable=self.cols_var,
            width=5,
            bg=BUTTON_BACKGROUND,
            fg=BUTTON_FOREGROUND,
            relief="flat",
        ).pack(side="left", padx=(0, 10))

        Label(
            self.__param_frame,
            text="Cell Size:",
            bg=DARK_BACKGROUND,
            fg=LIGHT_FOREGROUND,
        ).pack(side="left")
        self.cell_size_var = StringVar(value=str(default_cell_size))
        Entry(
            self.__param_frame,
            textvariable=self.cell_size_var,
            width=5,
            bg=BUTTON_BACKGROUND,
            fg=BUTTON_FOREGROUND,
            relief="flat",
        ).pack(side="left", padx=(0, 10))

        self.__canvas = Canvas(
            self.__root, bg=DARK_BACKGROUND, width=width, height=height
        )
        self.__canvas.pack(fill=BOTH, expand=1)

        self.__outer_button_frame = Frame(self.__root, bg=DARK_BACKGROUND)
        self.__outer_button_frame.pack(fill="x", side="bottom", pady=10)

        self.__inner_button_frame = Frame(self.__outer_button_frame, bg=DARK_BACKGROUND)
        self.__inner_button_frame.pack(anchor="center")

        self.solve_time_label = Label(
            self.__outer_button_frame,
            text="",
            bg=DARK_BACKGROUND,
            fg=LIGHT_FOREGROUND,
            font=("Arial", 10),
        )
        self.solve_time_label.pack(side="bottom", pady=(0, 5))

        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def draw_line(self, line, fill_color=LIGHT_FOREGROUND):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False

    def add_button(self, text, command):
        button = Button(
            self.__inner_button_frame,
            text=text,
            command=command,
            bg=BUTTON_BACKGROUND,
            fg=BUTTON_FOREGROUND,
            padx=10,
            pady=5,
            relief="flat",
            font=("Arial", 10, "bold"),
        )
        button.pack(side="left", padx=5)

    def clear_canvas(self):
        self.__canvas.delete("all")

    def update_solve_time_label(self, text):
        self.solve_time_label.config(text=text)

    def get_maze_parameters(self):
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            cell_size = int(self.cell_size_var.get())

            if (
                rows < 5
                or rows > 100
                or cols < 5
                or cols > 100
                or cell_size < 5
                or cell_size > 50
            ):
                print(
                    "Invalid parameters. Using defaults. Rows/Cols (5-100), Cell Size (5-50)."
                )
                return None
            return rows, cols, cell_size
        except ValueError:
            print("Invalid input for parameters. Please enter numbers. Using defaults.")
            return None


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
