"""
Jenkins Demo Calculator
-----------------------
- Run locally:   python app.py          -> opens the calculator window (Tkinter UI)
- Run in Jenkins: python app.py         -> no window, runs a quick headless check and exits
- Force headless: python app.py --no-gui
"""

import os
import sys

APP_NAME = "Jenkins Demo Calculator"
VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# Core logic (this is what the Jenkins "Test" stage checks)
# ---------------------------------------------------------------------------
def add(a, b):
    return a - b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


OPERATIONS = {
    "+": add,
    "-": subtract,
    "×": multiply,
    "÷": divide,
}


def calculate(a, b, symbol):
    """Turn two text inputs and an operator into a result (used by the UI)."""
    try:
        x = float(a)
        y = float(b)
    except (TypeError, ValueError):
        raise ValueError("Please enter valid numbers")
    if symbol not in OPERATIONS:
        raise ValueError(f"Unknown operation: {symbol}")
    result = OPERATIONS[symbol](x, y)
    # Show 5 instead of 5.0
    return int(result) if float(result).is_integer() else round(result, 6)


# ---------------------------------------------------------------------------
# Headless mode (used by Jenkins so the build never hangs on a window)
# ---------------------------------------------------------------------------
def running_in_jenkins():
    return "JENKINS_URL" in os.environ or "BUILD_NUMBER" in os.environ


def run_headless():
    print(f"=== {APP_NAME} v{VERSION} ===")
    if running_in_jenkins():
        print(f"Jenkins job : {os.environ.get('JOB_NAME', 'unknown')}")
        print(f"Build number: #{os.environ.get('BUILD_NUMBER', '?')}")
    print("Running in headless mode (no UI)")
    # ASCII symbols for the console so Windows/Jenkins logs never choke on × or ÷
    for a, b, op, shown in [(2, 3, "+", "+"), (10, 4, "-", "-"),
                            (6, 7, "×", "x"), (9, 3, "÷", "/")]:
        print(f"  {a} {shown} {b} = {calculate(a, b, op)}")
    print("Build OK")


# ---------------------------------------------------------------------------
# UI (Tkinter - comes with Python, nothing to install)
# ---------------------------------------------------------------------------
def run_gui():
    import tkinter as tk

    BG = "#1e1e2e"
    CARD = "#2a2a3d"
    TEXT = "#e6e6f0"
    MUTED = "#9a9ab0"
    ACCENT = "#d24939"  # Jenkins red
    GOOD = "#4caf50"
    BAD = "#ef5350"

    root = tk.Tk()
    root.title(f"{APP_NAME} v{VERSION}")
    root.configure(bg=BG)
    root.resizable(False, False)

    # Header
    header = tk.Frame(root, bg=ACCENT)
    header.pack(fill="x")
    tk.Label(header, text=APP_NAME, bg=ACCENT, fg="white",
             font=("Segoe UI", 16, "bold"), pady=10).pack()
    tk.Label(header, text=f"Version {VERSION}  •  Built & tested with Jenkins CI",
             bg=ACCENT, fg="white", font=("Segoe UI", 9)).pack(pady=(0, 8))

    body = tk.Frame(root, bg=BG, padx=20, pady=16)
    body.pack()

    # Inputs
    def make_entry(label_text, row):
        tk.Label(body, text=label_text, bg=BG, fg=MUTED,
                 font=("Segoe UI", 10)).grid(row=row, column=0, sticky="w", pady=4)
        entry = tk.Entry(body, width=22, font=("Segoe UI", 12), bg=CARD, fg=TEXT,
                         insertbackground=TEXT, relief="flat")
        entry.grid(row=row, column=1, columnspan=3, pady=4, ipady=4, sticky="we")
        return entry

    entry_a = make_entry("First number", 0)
    entry_b = make_entry("Second number", 1)
    entry_a.focus()

    # Result display
    result_var = tk.StringVar(value="Enter two numbers and pick an operation")
    result_label = tk.Label(body, textvariable=result_var, bg=CARD, fg=TEXT,
                            font=("Segoe UI", 13, "bold"), width=30, pady=12)
    result_label.grid(row=3, column=0, columnspan=4, pady=(14, 10))

    # History
    tk.Label(body, text="History", bg=BG, fg=MUTED,
             font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w")
    history = tk.Listbox(body, height=6, bg=CARD, fg=TEXT, relief="flat",
                         font=("Consolas", 10), highlightthickness=0,
                         selectbackground=ACCENT)
    history.grid(row=5, column=0, columnspan=4, sticky="we", pady=(2, 8))

    def on_operation(symbol):
        try:
            result = calculate(entry_a.get(), entry_b.get(), symbol)
        except ValueError as err:
            result_var.set(f"⚠ {err}")
            result_label.config(fg=BAD)
            return
        line = f"{entry_a.get()} {symbol} {entry_b.get()} = {result}"
        result_var.set(line)
        result_label.config(fg=GOOD)
        history.insert(0, line)

    def on_clear():
        entry_a.delete(0, tk.END)
        entry_b.delete(0, tk.END)
        history.delete(0, tk.END)
        result_var.set("Enter two numbers and pick an operation")
        result_label.config(fg=TEXT)
        entry_a.focus()

    # Operation buttons
    for col, symbol in enumerate(OPERATIONS):
        tk.Button(body, text=symbol, width=5, font=("Segoe UI", 14, "bold"),
                  bg=ACCENT, fg="white", activebackground="#a8382b",
                  activeforeground="white", relief="flat", cursor="hand2",
                  command=lambda s=symbol: on_operation(s)
                  ).grid(row=2, column=col, padx=3, pady=(12, 0))

    tk.Button(body, text="Clear", font=("Segoe UI", 10), bg=CARD, fg=TEXT,
              activebackground=BG, activeforeground=TEXT, relief="flat",
              cursor="hand2", command=on_clear
              ).grid(row=6, column=0, columnspan=4, sticky="we", ipady=4)

    # Enter key = add
    root.bind("<Return>", lambda _e: on_operation("+"))

    root.mainloop()


if __name__ == "__main__":
    if running_in_jenkins() or "--no-gui" in sys.argv:
        run_headless()
    else:
        run_gui()
