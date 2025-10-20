# gui_calculator.py
import tkinter as tk
import math
from typing import Any

# Safe evaluation dictionary
SAFE = {name: getattr(math, name) for name in dir(math) if not name.startswith("__")}
SAFE.update({
    "pi": math.pi,
    "e": math.e,
    "pow": pow,
    "abs": abs,
    "factorial": math.factorial
})

def safe_eval(expr: str) -> Any:
    if not expr.strip():
        return "0"
    expr = expr.replace("^", "**")  # allow ^ for power
    try:
        result = eval(expr, {"__builtins__": None}, SAFE)
        if isinstance(result, complex):
            return "Error: Complex result"
        return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except (SyntaxError, NameError):
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {str(e)}"

class SciCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("450x400")
        self.resizable(False, False)
        self.expression = ""
        self.create_widgets()
        self.bind_keys()

    def bind_keys(self):
        self.bind('<Return>', lambda e: self.on_button("="))
        self.bind('<BackSpace>', lambda e: self.on_button("⌫"))
        self.bind('<Delete>', lambda e: self.on_button("C"))
        self.bind('<Escape>', lambda e: self.quit())

    def create_widgets(self):
        self.display_var = tk.StringVar()
        entry = tk.Entry(
            self, 
            textvariable=self.display_var, 
            font=("Consolas", 18), 
            bd=10, 
            relief=tk.RIDGE, 
            justify="right"
        )
        entry.grid(row=0, column=0, columnspan=6, pady=10, padx=5, ipady=8, sticky="we")

        buttons = [
            ("7",1,0), ("8",1,1), ("9",1,2), ("/",1,3), ("sqrt",1,4), ("C",1,5),
            ("4",2,0), ("5",2,1), ("6",2,2), ("*",2,3), ("^",2,4), ("⌫",2,5),
            ("1",3,0), ("2",3,1), ("3",3,2), ("-",3,3), ("(",3,4), (")",3,5),
            ("0",4,0), (".",4,1), ("=",4,2), ("+",4,3), ("pi",4,4), ("e",4,5),
            ("sin",5,0), ("cos",5,1), ("tan",5,2), ("log",5,3), ("ln",5,4), ("fact",5,5)
        ]

        for (text, r, c) in buttons:
            btn = tk.Button(
                self,
                text=text,
                width=6,
                height=2,
                font=("Consolas", 14),
                command=lambda t=text: self.on_button(t)
            )
            btn.grid(row=r, column=c, padx=3, pady=3)

    def on_button(self, label):
        if label == "C":
            self.expression = ""
        elif label == "⌫":
            self.expression = self.expression[:-1]
        elif label == "=":
            expr = self.expression.replace("ln", "log").replace("fact", "factorial")
            result = safe_eval(expr)
            self.expression = str(result)
        elif label in ("sin", "cos", "tan", "log", "ln", "sqrt", "fact"):
            if label == "ln":
                self.expression += "log("
            elif label == "fact":
                self.expression += "factorial("
            else:
                self.expression += f"{label}("
        else:
            self.expression += label

        self.display_var.set(self.expression)

if __name__ == "__main__":
    try:
        app = SciCalculator()
        app.mainloop()
    except Exception as e:
        print(f"Error starting calculator: {e}")

