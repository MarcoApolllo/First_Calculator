import tkinter as tk
from tkinter import ttk

LARGE_FONT_STYLE = ("Arial", 32, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 22, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("280x450")

        self.current_expression_var = tk.StringVar(value="0")
        self.total_expression_var = tk.StringVar(value="")
        self.full_result = 0
        self.flag = False

        self.display = self.create_display_frame()
        self.total_label, self.current_label, self.history_button = self.create_labels()
        self.history = []
        self.buttons_frame = self.create_buttons_frame()
        self.operations = {"/": "÷", "*": "×", "-": "-", "+": "+"}
        self.create_buttons()
        self.bind_keys()

    def run(self):
        self.window.mainloop()

    def create_display_frame(self):
        style = ttk.Style()
        style.configure("Display.TFrame", background=LIGHT_GRAY)

        self.display = ttk.Frame(self.window, width=250, height=120, style="Display.TFrame")
        self.display.pack(expand=True, fill="both")

        return self.display

    def create_labels(self):
        # Create a top_frame inside your display to hold both widgets.
        top_frame = tk.Frame(self.display, bg=LIGHT_GRAY)
        top_frame.pack(side=tk.TOP, fill="x")

        # History button at the top left.
        self.history_button = tk.Button(
            top_frame,
            text="🕘",
            font=("Arial", 12),
            bg=LIGHT_GRAY,
            fg=LABEL_COLOR,
            command=self.show_history,
            borderwidth=0,
            width=2,
            height=1
        )
        self.history_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Total expression label next to the history button.
        self.total_label = tk.Label(
            top_frame,
            textvariable=self.total_expression_var,
            fg="#555555",
            font=SMALL_FONT_STYLE,
            bg=LIGHT_GRAY
        )
        self.total_label.pack(side=tk.RIGHT, padx=5, pady=5)

        # Current expression label at the top right.
        self.current_label = tk.Label(
            self.display,
            textvariable=self.current_expression_var,
            font=LARGE_FONT_STYLE,
            bg=LIGHT_GRAY
        )
        self.current_label.pack(anchor="e", padx=5, pady=5)

        return self.total_label, self.current_label, self.history_button

    def create_buttons_frame(self):
        self.buttons_frame = ttk.Frame(self.window, style="White.TFrame")
        self.buttons_frame.pack(fill="both", expand=True)

        return self.buttons_frame

    def create_buttons(self):
        buttons = [
            ("(", 1, 1), (")", 1, 2), ("C", 1, 3), ("←", 1, 4),
            ("%", 2, 1), ("x²", 2, 2), ("√x", 2, 3), ("÷", 2, 4),
            ("7", 3, 1), ("8", 3, 2), ("9", 3, 3), ("×", 3, 4),
            ("4", 4, 1), ("5", 4, 2), ("6", 4, 3), ("-", 4, 4),
            ("1", 5, 1), ("2", 5, 2), ("3", 5, 3), ("+", 5, 4),
            ("+/-", 6, 1), ("0", 6, 2), (".", 6, 3), ("=", 6, 4)
        ]

        operations = {
            "C": self.clear,
            "←": self.backspace,
            "%": self.percent,
            "+/-": self.toggle_sign,
            "÷": lambda: self.add_to_expression("÷"),
            "×": lambda: self.add_to_expression("×"),
            "-": lambda: self.add_to_expression("-"),
            "+": lambda: self.add_to_expression("+"),
            "(": lambda: self.add_to_expression("("),
            ")": lambda: self.add_to_expression(")"),
            "x²": self.square,
            "√x": self.sqrt,
            "=": self.evaluate
        }
        numbers = [str(i) for i in range(10)] + [".", "x²", "√x"]

        equals_button = None
        for (text, row, col) in buttons:
            if text in operations:
                command = operations[text]
            elif text in numbers:
                command = lambda value=text: self.add_to_expression(value)
            button = tk.Button(self.buttons_frame, text=text, bg=WHITE if text.isdigit() else OFF_WHITE, fg=LABEL_COLOR, activebackground="#E6E6E6" if text.isdigit() else "#DDE2E8", font=DIGITS_FONT_STYLE if text.isdigit() else DEFAULT_FONT_STYLE, borderwidth=0, padx=20, pady=20, relief="raised", command = command)
            button.grid(row=row, column=col, sticky="nsew", padx= 2/3, pady=2/3)
            if text == "=":
                equals_button = button

        if equals_button is not None:
            equals_button.config(bg="purple")

        for i in range(1, 7):
            self.buttons_frame.rowconfigure(i, weight=1)
        for j in range(1, 5):
            self.buttons_frame.columnconfigure(j, weight=1)

    def clear(self):
        if self.current_expression_var.get() == "0":
            self.total_expression_var.set("")
        else:
            self.current_expression_var.set("0")

    def backspace(self):
        current_expression = self.current_expression_var.get()
        if len(current_expression) > 0:
            self.current_expression_var.set(current_expression[:-1])

    def percent(self):
        self.current_expression_var.set(str(float(self.current_expression_var.get())*0.01))

    def toggle_sign(self):
        # self.current_expression_var.set(str(float(self.current_expression_var.get()) * (-1))) makes a bit less sense, though still works
        self.total_expression_var.set(f"-({self.current_expression_var.get()})")

    def square(self):
        current_value = self.current_expression_var.get()

        if current_value:
            self.total_expression_var.set(f"{self.total_expression_var.get() if self.total_expression_var.get() and self.flag == False else ""}sq({current_value})")
            self.current_expression_var.set("")

        else:
            self.total_expression_var.set(f"sq({self.total_expression_var.get()})")

        self.flag = True # so that the current_expression doesn't get added to the total_expression

    def sqrt(self):
        current_value = self.current_expression_var.get()

        if current_value:
            self.total_expression_var.set(f"{self.total_expression_var.get() if self.total_expression_var.get() and self.flag == False else ""}sqrt({current_value})")
            self.current_expression_var.set("")

        else:
            self.total_expression_var.set(f"sqrt({self.total_expression_var.get()})")

        self.flag = True # so that the current_expression doesn't get added to the total_expression

    def add_to_expression(self, value): # comma after zero
        if self.flag:
            self.current_expression_var.set("")

        if value.isdigit():
            if self.current_expression_var.get() == "0":
                self.current_expression_var.set(value)
            else:
                self.current_expression_var.set(self.current_expression_var.get() + value)

        elif value == ".":
            self.current_expression_var.set(self.current_expression_var.get() + value)

        else:
            contemporary_str = self.current_expression_var.get()
            self.current_expression_var.set("")
            self.total_expression_var.set(self.total_expression_var.get() + contemporary_str + value)

        self.flag = False

    def evaluate(self):
        total_expr = self.total_expression_var.get()
        current_expr = self.current_expression_var.get()


        if current_expr and not self.flag:
            if total_expr and total_expr[-1] in self.operations.values():
                total_expr += current_expr
            else:
                total_expr = current_expr

            self.total_expression_var.set(total_expr)
            self.current_expression_var.set("")

        try:
            total_expression = total_expr.replace("÷", "/").replace("×", "*")
            result = str(eval(total_expression, {"__builtins__": None}, {
                "sq": lambda x: x ** 2,
                "sqrt": lambda x: x ** 0.5
            }))
            self.history.append(f"{self.total_expression_var.get()} = {result}")
            self.current_expression_var.set(self.update_display(result))
            self.flag = True
        except Exception as e:
            self.current_expression_var.set("Error")
            print(e)

    def update_display(self, result):
        self.full_result = result

        try:
            number = float(result)
        except ValueError:
            self.current_expression_var.set(result)
            return

        int_part = result.split(".")[0]

        if len(int_part) > 10:
            display_value = "{:.6e}".format(number)
        else:
            display_value = result[:11]

        return display_value

    def bind_keys(self):
        for i in range(10):
            self.window.bind(str(i), lambda event, digit=i: self.add_to_expression(str(digit)))
        for button in ["(", ")", "."]:
            self.window.bind(button, lambda event, b=button: self.add_to_expression(b))

        for operator in self.operations.keys():
            self.window.bind(operator, lambda event, op=operator: self.add_to_expression(self.operations[op]))

        self.window.bind("<Return>", lambda event: self.evaluate())

    def show_history(self):
        history_window = tk.Toplevel(self.window)
        history_window.title("History")
        history_window.geometry("300x400")

        history_text = "\n".join(self.history[-10:])  # Show last 10 calculations
        label = tk.Label(history_window, text=history_text, font=("Arial", 14), justify=tk.LEFT)
        label.pack(padx=10, pady=10)


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
