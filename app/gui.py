from tkinter import *
from app.logic import calculate_expression
from app.logic import resource_path
import re

def start_app():

    win = Tk()
    win.title("Calculator")
    win.geometry('400x500+50+30')
    win.resizable(False,False)
    icon_path = resource_path('app/calculator_icon-icons.com_72046.ico')
    win.iconbitmap(icon_path)
    win.config(bg='#1e1e1e')


    def lighten_color(hex_color, factor=0.15):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))

        return f"#{r:02x}{g:02x}{b:02x}"

    def add_hover(widget, normal_bg):
        hover_bg = lighten_color(normal_bg, 0.18)

        widget.bind(
            "<Enter>",
            lambda e, hb=hover_bg: e.widget.config(bg=hb)
        )
        widget.bind(
            "<Leave>",
            lambda e, nb=normal_bg: e.widget.config(bg=nb)
        )

    def on_click(value):
        if value == "/":
            value = "÷"
        display.config(state="normal")
        display.insert(END, value)
        display.config(state="readonly")

    def on_clear():
        display.config(state="normal")
        display.delete(0, END)
        display.config(state="readonly")
        
    
    def on_backspace():
        display.config(state="normal")
        display.delete(len(display.get()) - 1, END)
        display.config(state="readonly")

    def on_equal():
        display.config(state="normal")
        result = calculate_expression(display.get())
        display.delete(0, END)
        display.insert(END, result)
        display.config(state="readonly")

    def sign_change():
        value = display.get()
        if not value:
            sign = "-"
        elif value and value[0] == "-":
            sign = "+"
        else:
            sign = "-"
        try:
            if value[0] in "+-":
                value = sign + value[1:]
        except IndexError:
            value = sign + value
        finally:
            display.config(state="normal")
            display.delete(0, END)
            display.insert(0, value)
            display.config(state="readonly")
    
    def open_brackets_count(exp):
        return exp.count("(") - exp.count(")")
    
    def insert_bracket():
        
        exp = display.get()
        display.config(state="normal")

        if exp == "":
            display.insert(END, "(")

        else:
            open_count = open_brackets_count(exp)
            last = exp[-1]

            # cases where LEFT bracket makes sense
            if last in "+-*/(":
                display.insert(END, "(")

            # cases where RIGHT bracket makes sense
            elif open_count > 0:
                display.insert(END, ")")

            else:
                display.insert(END, "(")

        display.config(state="readonly")



    def flash_button(btn, normal_bg):
        hover_bg = lighten_color(normal_bg, 0.18)
        btn.config(bg=hover_bg)
        btn.after(120, lambda: btn.config(bg=normal_bg))



    def key_press(event):
        key = event.char
        keysym = event.keysym

        # ---- ESC / DELETE → clear ----
        if keysym in ("Escape", "Delete"):
            on_clear()
            btn, bg = button_map["AC"]
            flash_button(btn, bg)
            return "break"

        # ---- BACKSPACE ----
        if keysym == "BackSpace":
            display.config(state="normal")
            display.delete(len(display.get()) - 1, END)
            display.config(state="readonly")
            btn, bg = button_map["C"]
            flash_button(btn, bg)
            return "break"

        # ------- ENTER --------
        if keysym in ("Return","equal"):
            on_equal()
            btn, bg = button_map["="]
            flash_button(btn, bg)
            return "break"
        #-----VALID INPUT------
        if key.isdigit() or key in "+-*/.%()":
            if key == "*":
                key = "x"
            on_click(key)
            if key in button_map:
                btn, bg = button_map[key]
                flash_button(btn, bg)
            return "break"
        return "break"
    
    display = Entry(
    win,
    font=("Bahnschrift SemiBold", 24),
    bg="#000000",
    fg="#00ffcc",
    bd=0,
    justify="right",
    state="readonly",
    readonlybackground="#000000"
    )
    display.pack(fill="x", ipady=15, pady=10, padx=10)
    display.focus_set()
    
    btn_frame = Frame(win, bg="#1e1e1e")
    btn_frame.pack(expand=True, fill="both")

    buttons = [
        ("AC", "#ff3b30"), ("( )", "#2d2d2d"), ("%", "#2d2d2d"), ("÷", "#ff9500"),
        ("7", "#2d2d2d"), ("8", "#2d2d2d"), ("9", "#2d2d2d"), ("x", "#ff9500"),
        ("4", "#2d2d2d"), ("5", "#2d2d2d"), ("6", "#2d2d2d"), ("-", "#ff9500"),
        ("1", "#2d2d2d"), ("2", "#2d2d2d"), ("3", "#2d2d2d"), ("+", "#ff9500"),
        (".", "#2d2d2d"), ("0", "#2d2d2d"), ("C", "#a25245"), ("=", "#33c62e")
    ]

    button_map = {}
    row = col = 0
    for text, color in buttons:
        font = ("Bahnschrift SemiBold", 24,'bold')
        if text == "=":
           cmd = on_equal
        elif text == "AC":
            font = ("Bahnschrift SemiBold", 20, "bold")
            cmd = on_clear
        elif text == "C":
            cmd = on_backspace
        elif text == "( )":
            cmd = insert_bracket
            font = ("Bahnschrift SemiBold", 20, "bold")
        else:
            cmd = lambda value= text : on_click(value)

        btn = Button(
            btn_frame,
            text=text,
            font=font,
            bg=color,
            fg="white",
            bd=0,
            command=cmd
        )

        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        add_hover(btn, color)
        button_map[text] = (btn, color)        


        col += 1
        if col == 4:
            col = 0
            row += 1

    for i in range(4):
        btn_frame.columnconfigure(i, weight=1)
    for i in range(5):
        btn_frame.rowconfigure(i, weight=1)
    
    win.bind("<KeyPress>", key_press)

    win.mainloop()