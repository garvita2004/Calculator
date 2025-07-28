import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.expression = ""

        self.entry = tk.Entry(root, font=("Arial", 24), borderwidth=3, relief="ridge", justify='right', state="readonly")
        self.entry.grid(row=0, column=0, columnspan=4, ipady=20, pady=10, padx=10, sticky="nsew")
        self.entry_var = tk.StringVar()
        self.entry.config(textvariable=self.entry_var)

        self.create_buttons()
        self.bind_keys()

    def create_buttons(self):
        buttons = [
            ("C", 1, 0), ("DEL", 1, 1), ("%", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("+/-", 5, 0), ("0", 5, 1), (".", 5, 2), ("=", 5, 3),
        ]

        for (text, row, col) in buttons:
            action = lambda x=text: self.on_click(x)
            tk.Button(self.root, text=text, width=5, height=2, font=("Arial", 18),
                      command=action).grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.root.grid_columnconfigure(j, weight=1)

    def bind_keys(self):
        self.root.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        char = event.char
        if char in "0123456789.+-*/%":
            self.expression += char
            self.update_display()
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.expression = self.expression[:-1]
            self.update_display()
        elif event.keysym.lower() == "c":
            self.clear()

    def on_click(self, char):
        if char == "C":
            self.clear()
        elif char == "DEL":
            self.expression = self.expression[:-1]
            self.update_display()
        elif char == "=":
            self.calculate()
        elif char == "+/-":
            self.toggle_sign()
        elif char == "%":
            self.apply_percentage()
        else:
            self.expression += str(char)
            self.update_display()

    def update_display(self):
        self.entry_var.set(self.expression)

    def clear(self):
        self.expression = ""
        self.update_display()

    def toggle_sign(self):
        try:
            if self.expression:
                tokens = self.expression.rstrip("+-*/")
                num = eval(tokens)
                num *= -1
                self.expression = str(num)
                self.update_display()
        except:
            self.entry_var.set("Error")

    def apply_percentage(self):
        try:
            if self.expression:
                tokens = self.expression.rstrip("+-*/")
                percent = eval(tokens) / 100
                self.expression = self.expression[:-len(tokens)] + str(percent)
                self.update_display()
        except:
            self.entry_var.set("Error")

    def calculate(self):
        try:
            # Avoid invalid starting expressions
            if self.expression[0] in "*/":
                raise Exception("Invalid start")
            result = eval(self.expression)
            self.expression = str(result)
            self.update_display()
        except ZeroDivisionError:
            self.entry_var.set("Error: DivBy0")
            self.expression = ""
        except:
            self.entry_var.set("Syntax Error")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
